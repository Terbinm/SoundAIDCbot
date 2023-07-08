import discord
import os
from discord.ext import commands
import datetime
import shutil
# import discord_downloader as dd

from discord_downloader.config import cfg
from discord_downloader.parser import base_parser
from discord_downloader.utils import (
    none_or_int,
    none_or_str,
    none_or_date,
    none_or_list,
)

discord_API_Token = "MTEyNjc3MjgwNzAxMTkzMDEyNA.GxNtaS.GRK2AGr7uXduCJbSJnVoSXPMhI07sAd6JppV90"
discord_AI_Room = '1069634244873310352'



def run_discord_bot(
    filetypes=none_or_str(cfg.get("args", "filetypes")),
    output_dir_set=str(cfg.get("args", "output_dir")), #設定目錄
    dry_run=cfg.getboolean("args", "dry_run"),
    verbose=cfg.getboolean("args", "verbose"),
    prepend_user=cfg.getboolean("args", "prepend_user"),
    include_str=none_or_str(cfg.get("args", "include_str")),
    exclude_str=none_or_str(cfg.get("args", "exclude_str")),
):
    
    # download_dir = datetime.datetime.now().strftime("%Y%m%d")
    download_dir = "test" #輸出檔案位置
    download_log_dir = "old_log" #輸出檔案位置(log)

    output_dir = os.path.join(output_dir_set, download_dir)
    output_log_dir = os.path.join(output_dir_set, download_log_dir)
    print(f" '{output_dir}' ({output_log_dir})")

    os.makedirs(output_dir, exist_ok=True) #創造out目錄
    os.makedirs(output_log_dir, exist_ok=True) #創造out_log目錄

    intents = discord.Intents.default()
    # Change your token here
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'機器人已上線!!! {client.user}')
        # filetypes=filetypes,
        # output_dir=output_dir,
        # prepend_user=prepend_user,
        # dry_run=dry_run,
        # include_str=include_str,
        # exclude_str=exclude_str,


    @client.event
    async def on_message(message):
        global AIconversation
        global ResponsesType
        if message.author == client.user:  #跳過自己的訊息
            return
            
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel.id)
        Answer = ''

        print(f"{username} 說: '{user_message}' ({channel})")
        print(f"==={message.attachments}===")
        if message.attachments:
            for a in message.attachments:
                # print(f" >> test ") #找到符合訊息
                if (
                    (
                        filetypes is None
                        or a.filename.split(".")[-1] in filetypes
                    )
                    and (
                        include_str is None or include_str in a.filename
                    )
                    and (
                        exclude_str is None
                        or exclude_str not in a.filename
                    )
                ):
                    if verbose:
                        print(f" > 已找到檔案: {a.filename}")
                    fname = (
                        message.author.name.replace(" ", "_")
                        + "__"
                        + a.filename
                        if prepend_user
                        else a.filename
                    )
                    
                    files = os.listdir(output_dir)

                    if len(files) > 0:
                        print('資料夾內有其他檔案，移動其他檔案')
                        for file_name in files:
                            source_file = os.path.join(output_dir, file_name)
                            destination_file = os.path.join(output_log_dir, file_name)
                            shutil.move(source_file, destination_file)
                    else:
                        print('資料夾內沒有其他檔案')

                    print(os.listdir(output_dir))
                    fname = os.path.join(output_dir, fname)
                    if not dry_run:
                        await a.save(fname)
            print(f"\n**** 已保存檔案於 {output_dir} 中")
            await message.channel.send(f"已經保存檔案:{fname}")


    client.run(discord_API_Token)


