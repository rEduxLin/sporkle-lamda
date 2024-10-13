from dataclasses import dataclass
from .DiscordTypes import Permissions
import requests
import time
import os

class Embedding:
    def __init__(self, title: str = "", desc: str = "", url: str = "", color: int = "", fields: list[dict] = [], footer: dict = {}):
        self.title = title
        self.desc = desc
        self.url = url
        self.color = color
        self.fields = fields
        self.footer = footer
    

    def to_dict(self):
        return {
            "title": self.title if self.title else None,
            "description": self.desc if self.desc else None,
            "url": self.url if self.url else None,
            "color": self.color if self.color else None,
            "fields": self.fields if self.fields else None,
            "footer": self.footer if self.footer else None
        }
    

    def set_title(self, title: str):
        self.title = title
    

    def set_description(self, desc: str):
        self.desc = desc


    def set_url(self, url: str):
        self.url = url
    

    def set_color(self, color: int):
        self.color = color
    

    def add_field(self, name: str, value: str, inline: bool):
        # NEVER use append() here 
        self.fields = self.fields + [{"name": name, "value": value, "inline": inline}]
    

    def set_footer(self, text: str, icon_url: str = None):
        self.footer = {"text": text, "icon_url": icon_url}

@dataclass
class PermissionOverwrite:
    id: str
    type: int
    allow: str
    deny: str

    @staticmethod
    def from_json(data: dict):
        id = data.get("id")
        type = data.get("type")
        allow = data.get("allow")
        deny = data.get("deny")

        return PermissionOverwrite(id, type, allow, deny)
    
    def is_allowed(self, permission: Permissions):
        return hex(self.allow) & permission == permission
    
    def is_denied(self, permission: Permissions):
        return hex(self.deny) & permission == permission
        

@dataclass
class Channel:
    id: str
    owner_id: str
    permission_overwrite_list: dict[str, PermissionOverwrite]

    @staticmethod
    def from_json(data: dict):
        id = data.get("id")
        owner_id = data.get("owner_id", 0)
        permission_overwrite_list = {
            permission_overwrite.get("id"): PermissionOverwrite.from_json(permission_overwrite) for permission_overwrite in data.get("permission_overwrites", {})
        }

        return Channel(id, owner_id, permission_overwrite_list)
        
    def set_permissions_overwrite(self, overwrite: PermissionOverwrite):
        url = "https://discord.com/api/v10//channels/{0}/permissions/{1}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bot {os.environ.get('BOT_TOKEN')}",
        }
        data = {
            "type": overwrite.type,
            "allow": overwrite.allow,
            "deny": overwrite.deny,
        }

        response = requests.put(url.format(self.id, overwrite.id), json=data, headers=headers)

        return response
    
    def lock_thread(self):
        url = f"https://discord.com/api/v10/channels/{self.id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bot {os.environ.get('BOT_TOKEN')}",
        }
        data = {
            "locked": True,
        }

        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            return ""
        else:
            return f"Error {response.status_code}: {response.text}"
    
    @staticmethod
    def get_by_id(target_id: int):
        url = "https://discord.com/api/v10/channels/{0}"
        headers = {
            "Authorization": f"Bot {os.environ.get('BOT_TOKEN')}"
        }
        response = requests.get(url.format(target_id), headers=headers)
        if response.status_code == 200:
            return Channel.from_json(response.json())
        else:
            return None

class User:
    def __init__(self, data: dict) -> None:
        self.id = data.get("id")

class Member:
    def __init__(self, data: dict) -> None:
        self.user = User(data.get("user", {}))

class Interaction:
    PING_RESPONSE = { "type": 1 }

    def __init__(self, interaction: dict, app_id: str) -> None:
        self.type = interaction.get("type")
        self.token = interaction.get("token")
        self.id = interaction.get("id")
        self.data = interaction.get("data")
        self.timestamp = time.time()
        self.guild_id = interaction.get("guild_id")
        self.channel = Channel.from_json(interaction.get("channel", {}))
        self.author_id = interaction.get("member").get("user").get("id")

        self.callback_url = f"https://discord.com/api/v10/interactions/{self.id}/{self.token}/callback"
        self.webhook_url = f"https://discord.com/api/v10/webhooks/{app_id}/{self.token}/messages/@original"

    

    def __create_channel_message(self, content: str = None, embeds: list[Embedding] = None, ephemeral: bool = True) -> dict:
        response = {
            "content": content,
            "embeds": [embed.to_dict() for embed in embeds] if embeds else None,
            "flags": 1 << 6 if ephemeral else None
        }
        return response


    def defer(self, ephemeral: bool = True) -> None:
        try:
            requests.post(self.callback_url, json={"type": 5, "data": {"flags": 1 << 6 if ephemeral else None}}).raise_for_status()
        except Exception as e:
            raise Exception(f"Unable to defer response: {e}")
    

    def send_response(self, content: str = None, embeds: list[Embedding] = None, ephemeral: bool = True) -> None:
        try:
            requests.patch(self.webhook_url, json=self.__create_channel_message(content, embeds, ephemeral)).raise_for_status()
        except Exception as e:
            raise Exception(f"Unable to send response: {e}")


    def send_followup(self, content: str = None, embeds: list[Embedding] = None, ephemeral: bool = True) -> None:
        try:
            requests.post(self.webhook_url, json=self.__create_channel_message(content, embeds, ephemeral)).raise_for_status()
        except Exception as e:
            raise Exception(f"Unable to send followup: {e}")
