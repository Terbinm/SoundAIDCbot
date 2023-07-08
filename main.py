import bot as Aibot
from discord_downloader.parser import base_parser
import sys
# import mariadb
AiCtxLibrary = {}
if __name__ == '__main__':
    # SQLf.initializedb()
    
    parser = base_parser
    args = parser.parse_args()

    Aibot.run_discord_bot(
        filetypes=args.filetypes,
        output_dir_set=args.output_dir,
        dry_run=args.dry_run,
        verbose=args.verbose,
        prepend_user=args.prepend_user,
        include_str=args.include_str,
        exclude_str=args.exclude_str,
    )
    
