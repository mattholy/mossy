# -*- encoding: utf-8 -*-
'''
endpoint.py
----
Instance v1 api endpoint


@Time    :   2024/05/07 13:26:26
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils.model.instance import InstanceV1

router = APIRouter(prefix='/instance', tags=['API', 'v1'])


@router.get('', deprecated=True, response_class=JSONResponse)
def fetch_instance():
    true = True
    false = False
    null = None
    return JSONResponse({
        "uri": "test-mac.kryta.app",
        "title": "寒石百货  -  BLACK",
        "short_description": "我们欢迎任何语言，并且致力于提供人类最原始的快乐——围着一堆篝火聊天。Everyone is welcome.",
        "description": "",
        "email": "kryta@kryta.app",
        "version": "4.2.8",
        "urls": {
            "streaming_api": "wss://test-mac.kryta.app"
        },
        "stats": {
            "user_count": 32,
            "status_count": 1041,
            "domain_count": 4971
        },
        "thumbnail": "https://test-mac.kryta.app/system/site_uploads/files/000/000/001/@1x/f5b2eaf823221de8.png",
        "languages": [
            "en"
        ],
        "registrations": true,
        "approval_required": false,
        "invites_enabled": true,
        "configuration": {
            "accounts": {
                "max_featured_tags": 10
            },
            "statuses": {
                "max_characters": 500,
                "max_media_attachments": 4,
                "characters_reserved_per_url": 23
            },
            "media_attachments": {
                "supported_mime_types": [
                    "image/jpeg",
                    "image/png",
                    "image/gif",
                    "image/heic",
                    "image/heif",
                    "image/webp",
                    "image/avif",
                    "video/webm",
                    "video/mp4",
                    "video/quicktime",
                    "video/ogg",
                    "audio/wave",
                    "audio/wav",
                    "audio/x-wav",
                    "audio/x-pn-wave",
                    "audio/vnd.wave",
                    "audio/ogg",
                    "audio/vorbis",
                    "audio/mpeg",
                    "audio/mp3",
                    "audio/webm",
                    "audio/flac",
                    "audio/aac",
                    "audio/m4a",
                    "audio/x-m4a",
                    "audio/mp4",
                    "audio/3gpp",
                    "video/x-ms-asf"
                ],
                "image_size_limit": 16777216,
                "image_matrix_limit": 33177600,
                "video_size_limit": 103809024,
                "video_frame_rate_limit": 120,
                "video_matrix_limit": 8294400
            },
            "polls": {
                "max_options": 4,
                "max_characters_per_option": 50,
                "min_expiration": 300,
                "max_expiration": 2629746
            }
        },
        "contact_account": {
            "id": "109810711024380026",
            "username": "zen",
            "acct": "zen",
            "display_name": "Hanshi",
            "locked": false,
            "bot": true,
            "discoverable": true,
            "group": false,
            "created_at": "2023-02-05T00:00:00.000Z",
            "note": "<p>We are committed to an open and shared internet.</p>",
            "url": "https://test-mac.kryta.app/@zen",
            "uri": "https://test-mac.kryta.app/users/zen",
            "avatar": "https://test-mac.kryta.app/system/accounts/avatars/109/810/711/024/380/026/original/81f504fb5384ff1d.jpeg",
            "avatar_static": "https://test-mac.kryta.app/system/accounts/avatars/109/810/711/024/380/026/original/81f504fb5384ff1d.jpeg",
            "header": "https://test-mac.kryta.app/headers/original/missing.png",
            "header_static": "https://test-mac.kryta.app/headers/original/missing.png",
            "followers_count": 0,
            "following_count": 0,
            "statuses_count": 7,
            "last_status_at": "2024-03-05",
            "noindex": false,
            "emojis": [],
            "roles": [
                {
                    "id": "3",
                    "name": "创始人",
                    "color": "#fff833"
                }
            ],
            "fields": [
                {
                    "name": "We Host",
                    "value": "<a href=\"https://test-mac.kryta.app\" target=\"_blank\" rel=\"nofollow noopener noreferrer me\" translate=\"no\"><span class=\"invisible\">https://</span><span class=\"\">test-mac.kryta.app</span><span class=\"invisible\"></span></a>",
                    "verified_at": null
                },
                {
                    "name": "We Believe",
                    "value": "Everyone has the right to express their opinions",
                    "verified_at": null
                },
                {
                    "name": "We Welcome",
                    "value": "Mankind",
                    "verified_at": null
                },
                {
                    "name": "The Relay",
                    "value": "<a href=\"https://board.kryta.app\" target=\"_blank\" rel=\"nofollow noopener noreferrer me\" translate=\"no\"><span class=\"invisible\">https://</span><span class=\"\">board.kryta.app</span><span class=\"invisible\"></span></a>",
                    "verified_at": null
                }
            ]
        },
        "rules": [
            {
                "id": "6",
                "text": "严禁发布任何形式的儿童色情及恐怖主义内容，一经发现立即永久封禁。\r\nThe distribution of any form of child pornography or terrorism-related content is strictly forbidden and will lead to an immediate permanent ban."
            },
            {
                "id": "7",
                "text": "请利用内容警告功能对NSFW内容进行隐藏处理。\r\nPlease conceal NSFW content by employing the content warning feature."
            },
            {
                "id": "8",
                "text": "禁止发布虚假信息。请注意，寒石百货不对信息的真实性负责，用户需自行判断信息的真伪。\r\nRefrain from posting false information. Be aware that Hanshi does not verify the veracity of the content, and it is the responsibility of each user to evaluate its authenticity independently."
            },
            {
                "id": "9",
                "text": "寒石百货坚信合作与共享是互联网的根本，因此不主张也不提供知识产权保护。\r\nOur belief is rooted in the principle that cooperation and sharing are the cornerstones of the internet; as such, we neither advocate for nor offer protection of intellectual property rights."
            },
            {
                "id": "11",
                "text": "在寒石百货，您的性别或性取向并不重要，请勿过分强调这一点。\r\nAt Hanshi, your gender or sexual orientation is of no concern; please refrain from placing undue emphasis on this aspect."
            },
            {
                "id": "12",
                "text": "在讨论中，请基于理性论证，避免人身攻击。\r\nDuring discussions, please base your arguments on reason and refrain from personal attacks."
            }
        ]
    })
