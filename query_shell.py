#!/usr/bin/env python3
from __future__ import annotations
import inspect
import os, argparse, cmd2
from cmd2 import with_argparser  # pip install cmd2

import database, util, log

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

    # aliases for clean exit
    def do_quit(self, _):  return True
    do_q = do_exit = do_stop = do_quit

    # clear screen (cmd2 has built-in shell integration; keeping explicit cmd)
    def do_clear(self, _):
        """Clear the terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')
        self._cmdloop()  # cmd2 utility to refresh prompt
    do_cls = do_clear  # alias for clear command
