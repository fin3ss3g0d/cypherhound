#!/usr/bin/env python3
from __future__ import annotations
import inspect
import os, argparse, cmd2
from cmd2 import with_argparser  # pip install cmd2

import database, util, log

# ---------- helpers -------------------------------------------------
def _id_list(value: str) -> list[int]:
    """
    Parse a single CLI token into a list of ints.
    Accepts comma-separated values and ranges, e.g. 1,3,5-7
    """
    ids: set[int] = set()
    for part in value.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            ids.update(range(int(a), int(b) + 1))
        else:
            ids.add(int(part))
    if not ids:
        raise argparse.ArgumentTypeError('no valid IDs found')
    return sorted(ids)

class QueryShell(cmd2.Cmd):
    prompt = ': '

    def __init__(
        self,
        user: str,
        pwd: str,
        db: str,
        yaml_file: str,
        *,
        persistent_history_file: str | None = None,
        persistent_history_length: int = 1000,
    ) -> None:

        # ---------------- choose kwargs supported by *this* cmd2 version ----------
        base_kwargs = {
            "persistent_history_file": persistent_history_file,
            "persistent_history_length": persistent_history_length,
            "allow_cli_args": False,  # disable cmd2's CLI args handling
        }

        sig = inspect.signature(cmd2.Cmd.__init__)
        if "include_ipy" in sig.parameters:
            base_kwargs["include_ipy"] = False
        elif "use_ipython" in sig.parameters:          # very old cmd2 (≤ 1.x)
            base_kwargs["use_ipython"] = False

        super().__init__(**base_kwargs)

        self.driver = database.Driver(user, pwd, db, template_file=yaml_file)


    # --------- helpers ----------------------------------------------------
    def _validate_and_call(self, setter, value, label):
        """
        Common validation wrapper.
        """
        if not util.validate_common_config(value):
            self.perror(f'{label} is empty or missing "@!"')
            return
        util.validate_user_input(value)
        setter(value)
        log.log_successful_set(label, value)

    # --------- `set` command ----------------------------------------------
    set_parser = argparse.ArgumentParser(
        prog='set', description='Update query parameters')
    set_sub = set_parser.add_subparsers(dest='kind', required=True)

    for kind in ('user', 'group', 'computer', 'regex'):
        p = set_sub.add_parser(kind)
        p.add_argument('value', nargs='+', help=f'{kind} value')

    @with_argparser(set_parser)
    def do_set(self, args: argparse.Namespace):
        """Set user/group/computer/regex parameters."""
        value = ' '.join(args.value)
        match args.kind:
            case 'user':
                self._validate_and_call(self.driver.set_user_param, value, 'user')
            case 'group':
                self._validate_and_call(self.driver.set_group_param, value, 'group')
            case 'computer':
                self._validate_and_call(self.driver.set_computer_param, value, 'computer')
            case 'regex':
                self._validate_and_call(self.driver.set_regex, value, 'regex')

    # --------- `run` command ----------------------------------------------
    run_parser = argparse.ArgumentParser(prog='run', description='Execute a query')
    run_parser.add_argument('index', type=int, help='Query number to run')

    @with_argparser(run_parser)
    def do_run(self, args):
        """Run a stored query by numeric index."""
        if not 1 <= args.index <= len(self.driver.queries):
            self.perror('Index out of range')
            return
        self.driver.run_query(str(args.index), '')

    # --------- `export` command -------------------------------------------
    export_parser = argparse.ArgumentParser(
        prog='export', description='Run a query and save its results')
    export_parser.add_argument('index', type=int)
    export_parser.add_argument('-o', '--output', help='Output file name', required=True)

    @with_argparser(export_parser)
    def do_export(self, args):
        """Run a query and export its results to a file."""
        if not 1 <= args.index <= len(self.driver.queries):
            self.perror('Index out of range')
            return
        outfile = util.validate_export_command(args.output)
        self.driver.run_query(str(args.index), outfile)

    # --- list/search/quit map directly to driver methods ------------------
    list_parser = argparse.ArgumentParser(prog='list')
    list_parser.add_argument('group')

    @with_argparser(list_parser)
    def do_list(self, args):
        """List queries by group."""
        if not util.validate_list_command(args.group):
            self.perror('Invalid group')
            return
        self.driver.print_queries_by_group(args.group)

    def do_search(self, arg):
        """Full-text search through stored queries."""
        if not arg:
            self.perror('search <text>')
            return
        self.driver.search_queries(arg)

    # ---------- `report` command ---------------------------------------
    report_parser = argparse.ArgumentParser(
        prog='report',
        description='Run multiple queries and generate a HTML report'
    )
    report_parser.add_argument(
        'ids',
        nargs='*',          # 0 → ALL queries, ≥1 → selected
        type=_id_list,
        metavar='ID[,ID|ID-ID] ...',
        help=('IDs of queries to include. '
              'You can pass multiple tokens and use ranges, '
              'e.g. "1 3 5-7".  If omitted, every stored query is run.')
    )
    report_parser.add_argument(
        '-o', '--output',
        default='reports',
        metavar='DIR',
        help='Base directory where the HTML report folder will be created '
             '(default: %(default)s)'
    )
    report_parser.add_argument(
        '--open',
        action='store_true',
        help='Open the generated index.html in your default browser'
    )

    @with_argparser(report_parser)
    def do_report(self, args: argparse.Namespace):
        """Execute one or many queries → Bootstrap-styled HTML report."""
        # Flatten `ids` list of lists ⇢ single sorted list
        flat_ids = sorted({i for sub in args.ids for i in sub}) if args.ids else None

        # Sanity-check IDs
        if flat_ids and (min(flat_ids) < 1 or max(flat_ids) > len(self.driver.queries)):
            self.perror('One or more IDs are out of range')
            return

        try:
            self.driver.run_queries_to_html(
                query_ids=[str(i) for i in flat_ids] if flat_ids else None,
                report_root=args.output
            )
            if args.open:
                import webbrowser, pathlib
                idx = pathlib.Path(args.output).resolve().joinpath(
                    max(os.listdir(args.output))  # newest timestamped dir
                ).joinpath('index.html')
                webbrowser.open_new_tab(idx.as_uri())
        except Exception as e:
            self.perror(str(e))

    # aliases for clean exit
    def do_quit(self, _):  return True
    do_q = do_exit = do_stop = do_quit

    # clear screen (cmd2 has built-in shell integration; keeping explicit cmd)
    def do_clear(self, _):
        """Clear the terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')
        self._cmdloop()  # cmd2 utility to refresh prompt
    do_cls = do_clear  # alias for clear command
