# Telegram Bot API 10.4 — Complete Methods Catalog (186 Methods)

- **Verified Against:** Bot API 10.4 (November 9, 2026)
- **Verification Date:** November 11, 2026
- **Primary Source:** [Telegram Bot API Specification](https://core.telegram.org/bots/api)
- **Changelog Source:** [Bot API Changelog](https://core.telegram.org/bots/api-changelog)

This file catalogs all **186 methods** in Bot API 10.4 with their required/optional parameters (`?` denotes optional), return types, purpose, version history, and canonical anchor link.

---

## Getting Updates (4 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`getUpdates`](https://core.telegram.org/bots/api#getupdates) | `offset?, limit? (1-100), timeout?, allowed_updates?` | `Array of Update` | Long polling for incoming updates (conflicts with active webhook; returns 409 if webhook is set). | Bot API 1.0 (updated 10.4) |
| [`setWebhook`](https://core.telegram.org/bots/api#setwebhook) | `url, certificate?, ip_address?, max_connections? (1-100, up to 100000 on local server), allowed_updates?, drop_pending_updates?, secret_token? (1-256 chars)` | `Boolean (True)` | Registers an HTTPS webhook URL (ports 443, 80, 88, 8443; any port on local server). | Bot API 1.0 (updated 10.4) |
| [`deleteWebhook`](https://core.telegram.org/bots/api#deletewebhook) | `drop_pending_updates?` | `Boolean (True)` | Removes webhook integration and switches back to getUpdates. | Bot API 2.0 (updated 5.0) |
| [`getWebhookInfo`](https://core.telegram.org/bots/api#getwebhookinfo) | `None` | `WebhookInfo` | Returns current webhook status, pending update count, and last error details. | Bot API 2.1 |

## Bot Identity & Config (3 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`getMe`](https://core.telegram.org/bots/api#getme) | `None` | `User` | Returns basic information about the bot as a User object (including can_connect_to_business, has_main_web_app, allows_users_to_create_topics). | Bot API 1.0 (updated 9.4) |
| [`logOut`](https://core.telegram.org/bots/api#logout) | `None` | `Boolean (True)` | Logs out from the cloud Bot API server before launching the bot locally (10-minute cooldown before re-login). | Bot API 5.0 |
| [`close`](https://core.telegram.org/bots/api#close) | `None` | `Boolean (True)` | Closes the bot instance on a local server before moving it to another local server. | Bot API 5.0 |

## Sending Messages (6 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`sendMessage`](https://core.telegram.org/bots/api#sendmessage) | `chat_id, text (1-4096 chars), business_connection_id?, message_thread_id?, direct_messages_topic_id?, parse_mode?, entities?, link_preview_options?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends a text message (up to 4096 UTF-8 chars after entity parsing). | Bot API 1.0 (updated 10.3) |
| [`sendEphemeralMessage`](https://core.telegram.org/bots/api#sendephemeralmessage) | `chat_id?, receiver_user_id?, message (EphemeralMessageParameters)` | `Boolean (True)` | Sends a temporary client-side ephemeral message visible only to receiver_user_id in chat_id. | Bot API 10.3 (updated 10.4) |
| [`forwardMessage`](https://core.telegram.org/bots/api#forwardmessage) | `chat_id, from_chat_id, message_id, message_thread_id?, direct_messages_topic_id?, video_start_timestamp?, disable_notification?, protect_content?, message_effect_id?, suggested_post_parameters?` | `Message` | Forwards any message of any kind (service messages and protected messages cannot be forwarded). | Bot API 1.0 (updated 9.3) |
| [`forwardMessages`](https://core.telegram.org/bots/api#forwardmessages) | `chat_id, from_chat_id, message_ids (1-100 increasing IDs), message_thread_id?, direct_messages_topic_id?, disable_notification?, protect_content?` | `Array of MessageId` | Forwards up to 100 messages at once in increasing message_id order. | Bot API 7.0 (updated 9.2) |
| [`copyMessage`](https://core.telegram.org/bots/api#copymessage) | `chat_id, from_chat_id, message_id, message_thread_id?, direct_messages_topic_id?, video_start_timestamp?, caption?, parse_mode?, caption_entities?, show_caption_above_media?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `MessageId` | Copies a message without the 'Forwarded from' header and returns the new MessageId. | Bot API 5.0 (updated 9.3) |
| [`copyMessages`](https://core.telegram.org/bots/api#copymessages) | `chat_id, from_chat_id, message_ids (1-100 increasing IDs), message_thread_id?, direct_messages_topic_id?, disable_notification?, protect_content?, remove_caption?` | `Array of MessageId` | Copies up to 100 messages at once without forward headers. | Bot API 7.0 (updated 9.2) |

## Sending Media (9 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`sendPhoto`](https://core.telegram.org/bots/api#sendphoto) | `chat_id, photo (InputFile|String), business_connection_id?, message_thread_id?, direct_messages_topic_id?, caption? (0-1024), parse_mode?, caption_entities?, show_caption_above_media?, has_spoiler?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends a photo (max 10 MB, width + height <= 10000, aspect ratio <= 20). | Bot API 1.0 (updated 9.2) |
| [`sendAudio`](https://core.telegram.org/bots/api#sendaudio) | `chat_id, audio (InputFile|String), business_connection_id?, message_thread_id?, direct_messages_topic_id?, caption?, parse_mode?, caption_entities?, duration?, performer?, title?, thumbnail?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends an MP3/M4A audio file to be displayed in the music player (up to 50 MB cloud / 2000 MB local). | Bot API 1.0 (updated 9.2) |
| [`sendDocument`](https://core.telegram.org/bots/api#senddocument) | `chat_id, document (InputFile|String), business_connection_id?, message_thread_id?, direct_messages_topic_id?, thumbnail?, caption?, parse_mode?, caption_entities?, disable_content_type_detection?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends a general file (up to 50 MB cloud / 2000 MB local). | Bot API 1.0 (updated 9.2) |
| [`sendVideo`](https://core.telegram.org/bots/api#sendvideo) | `chat_id, video (InputFile|String), business_connection_id?, message_thread_id?, direct_messages_topic_id?, duration?, width?, height?, thumbnail?, cover?, start_timestamp?, caption?, parse_mode?, caption_entities?, show_caption_above_media?, has_spoiler?, supports_streaming?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends an MP4 video (returns message_id=0 in channels if >100 MB pending transcoding). | Bot API 1.0 (updated 9.2) |
| [`sendAnimation`](https://core.telegram.org/bots/api#sendanimation) | `chat_id, animation (InputFile|String), business_connection_id?, message_thread_id?, direct_messages_topic_id?, duration?, width?, height?, thumbnail?, caption?, parse_mode?, caption_entities?, show_caption_above_media?, has_spoiler?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends a GIF or H.264/MPEG-4 AVC soundless animation. | Bot API 4.0 (updated 9.2) |
| [`sendVoice`](https://core.telegram.org/bots/api#sendvoice) | `chat_id, voice (InputFile|String), business_connection_id?, message_thread_id?, direct_messages_topic_id?, caption?, parse_mode?, caption_entities?, duration?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends an OGG/Opus, MP3, or M4A voice message. | Bot API 1.0 (updated 9.2) |
| [`sendVideoNote`](https://core.telegram.org/bots/api#sendvideonote) | `chat_id, video_note (InputFile|String), business_connection_id?, message_thread_id?, direct_messages_topic_id?, duration?, length?, thumbnail?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends a rounded square MP4 video note (up to 1 minute long). | Bot API 3.0 (updated 9.2) |
| [`sendPaidMedia`](https://core.telegram.org/bots/api#sendpaidmedia) | `chat_id, star_count (1-25000), media (1-10 InputPaidMedia), business_connection_id?, message_thread_id?, direct_messages_topic_id?, payload? (0-128B), caption?, parse_mode?, caption_entities?, show_caption_above_media?, disable_notification?, protect_content?, allow_paid_broadcast?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends paid photos/videos unlocked by Telegram Stars (1-25000 XTR). | Bot API 7.6 (updated 9.3) |
| [`sendMediaGroup`](https://core.telegram.org/bots/api#sendmediagroup) | `chat_id, media (2-10 InputMediaAudio|Document|Photo|Video), business_connection_id?, message_thread_id?, direct_messages_topic_id?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, reply_parameters?` | `Array of Message` | Sends an album of 2 to 10 photos, videos, documents, or audio files. | Bot API 3.5 (updated 9.2) |

## Location & Contacts (3 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`sendLocation`](https://core.telegram.org/bots/api#sendlocation) | `chat_id, latitude, longitude, business_connection_id?, message_thread_id?, direct_messages_topic_id?, horizontal_accuracy? (0-1500m), live_period? (60-86400s or 0x7FFFFFFF), heading? (1-360), proximity_alert_radius? (1-100000m), disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends a static or live geographic location point. | Bot API 1.0 (updated 9.2) |
| [`sendVenue`](https://core.telegram.org/bots/api#sendvenue) | `chat_id, latitude, longitude, title, address, business_connection_id?, message_thread_id?, direct_messages_topic_id?, foursquare_id?, foursquare_type?, google_place_id?, google_place_type?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends information about a physical venue. | Bot API 2.0 (updated 9.2) |
| [`sendContact`](https://core.telegram.org/bots/api#sendcontact) | `chat_id, phone_number, first_name, last_name?, vcard?, business_connection_id?, message_thread_id?, direct_messages_topic_id?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends a phone contact with optional vCard. | Bot API 2.0 (updated 9.2) |

## Polls, Checklists & Dice (3 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`sendPoll`](https://core.telegram.org/bots/api#sendpoll) | `chat_id, question (1-300), options (2-12 InputPollOption), business_connection_id?, message_thread_id?, direct_messages_topic_id?, question_parse_mode?, question_entities?, is_anonymous?, type? ('quiz'|'regular'), allows_multiple_answers?, allows_revoting?, shuffle_options?, allow_adding_options?, hide_results_until_closes?, correct_option_ids?, explanation?, explanation_parse_mode?, explanation_entities?, open_period? (5-2628000s), close_date?, is_closed?, description? (0-1024), description_parse_mode?, description_entities?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, reply_parameters?, reply_markup?` | `Message` | Sends a native poll or multi-answer quiz (up to 12 options; open_period up to 30 days in 9.6+). | Bot API 4.2 (updated 9.6) |
| [`sendChecklist`](https://core.telegram.org/bots/api#sendchecklist) | `business_connection_id, chat_id, checklist (InputChecklist), disable_notification?, protect_content?, message_effect_id?, reply_parameters?, reply_markup?` | `Message` | Sends an interactive task checklist on behalf of a connected business account. | Bot API 9.1 |
| [`sendDice`](https://core.telegram.org/bots/api#senddice) | `chat_id, emoji? ('🎲'|'🎯'|'🏀'|'⚽'|'🎳'|'🎰'), business_connection_id?, message_thread_id?, direct_messages_topic_id?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends an animated random dice/darts/slot machine message (value 1-6 or 1-64). | Bot API 4.7 (updated 9.2) |

## Drafts, Actions & Reactions (3 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`sendMessageDraft`](https://core.telegram.org/bots/api#sendmessagedraft) | `chat_id, draft_id (non-zero int), text (1-4096), message_thread_id?, parse_mode?, entities?` | `Boolean (True)` | Streams a partial message draft to a user while generating a response (Bot API 9.3+; enabled for all bots in 9.5). | Bot API 9.3 (updated 9.5) |
| [`sendChatAction`](https://core.telegram.org/bots/api#sendchataction) | `chat_id, action ('typing'|'upload_photo'|'record_video'|'upload_video'|'record_voice'|'upload_voice'|'upload_document'|'choose_sticker'|'find_location'|'record_video_note'|'upload_video_note'), business_connection_id?, message_thread_id?` | `Boolean (True)` | Broadcasts a 5-second status indicator (e.g., typing...) in the chat header. | Bot API 1.0 (updated 7.2) |
| [`setMessageReaction`](https://core.telegram.org/bots/api#setmessagereaction) | `chat_id, message_id, reaction? (Array of ReactionType, max 1 for non-Premium bots), is_big?` | `Boolean (True)` | Sets, changes, or clears the bot's reaction on a message. | Bot API 7.0 |

## In-Chat HTML Widgets (10.4) (3 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`sendWidget`](https://core.telegram.org/bots/api#sendwidget) | `chat_id, url (HTTPS), message_thread_id?, direct_messages_topic_id?, aspect_ratio? ('1:1'|'2:1'|'3:2'|'4:3'|'16:9'|'16:10'), data? (0-4096 chars), disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, reply_parameters?, reply_markup?` | `Message` | Sends a sandboxed per-user interactive HTML widget iframe inside a chat. | Bot API 10.4 |
| [`sendSharedWidget`](https://core.telegram.org/bots/api#sendsharedwidget) | `chat_id, url (HTTPS), message_thread_id?, direct_messages_topic_id?, aspect_ratio?, data? (0-4096 chars), disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, reply_parameters?, reply_markup?` | `Message` | Sends a shared interactive HTML widget whose state updates for all chat participants. | Bot API 10.4 |
| [`answerWidgetQuery`](https://core.telegram.org/bots/api#answerwidgetquery) | `widget_query_id, data? (0-4096 chars), ephemeral_message? (EphemeralMessageParameters)` | `Boolean (True)` | Answers a WidgetQuery or SharedWidgetQuery emitted by window.TelegramWidget.sendQuery. | Bot API 10.4 |

## Users, Profiles & Files (4 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`getUserProfilePhotos`](https://core.telegram.org/bots/api#getuserprofilephotos) | `user_id, offset?, limit? (1-100)` | `UserProfilePhotos` | Returns a list of profile pictures for a user. | Bot API 1.0 |
| [`getUserProfileAudios`](https://core.telegram.org/bots/api#getuserprofileaudios) | `user_id, offset?, limit? (1-100)` | `UserProfileAudios` | Returns a list of audio tracks added to a user's profile. | Bot API 9.4 |
| [`setUserEmojiStatus`](https://core.telegram.org/bots/api#setuseremojistatus) | `user_id, emoji_status_custom_emoji_id?, emoji_status_expiration_date?` | `Boolean (True)` | Changes a user's custom emoji status (requires user approval via Mini App requestEmojiStatusAccess). | Bot API 8.0 |
| [`getFile`](https://core.telegram.org/bots/api#getfile) | `file_id` | `File` | Prepares a file for download and returns file_path (up to 20 MB on cloud, 4000 MB on local server; link valid >= 1 hour). | Bot API 1.0 |

## Chat Member Moderation (8 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`banChatMember`](https://core.telegram.org/bots/api#banchatmember) | `chat_id, user_id, until_date?, revoke_messages?` | `Boolean (True)` | Bans a user in a group, supergroup, or channel (forever if until_date < +30s or > +366d). | Bot API 5.3 |
| [`unbanChatMember`](https://core.telegram.org/bots/api#unbanchatmember) | `chat_id, user_id, only_if_banned?` | `Boolean (True)` | Unbans a previously banned user in a supergroup or channel. | Bot API 1.0 |
| [`restrictChatMember`](https://core.telegram.org/bots/api#restrictchatmember) | `chat_id, user_id, permissions (ChatPermissions), use_independent_chat_permissions?, until_date?` | `Boolean (True)` | Restricts a user in a supergroup according to ChatPermissions. | Bot API 3.1 (updated 6.5) |
| [`promoteChatMember`](https://core.telegram.org/bots/api#promotechatmember) | `chat_id, user_id, is_anonymous?, can_manage_chat?, can_delete_messages?, can_manage_video_chats?, can_restrict_members?, can_promote_members?, can_change_info?, can_invite_users?, can_post_stories?, can_edit_stories?, can_delete_stories?, can_post_messages?, can_edit_messages?, can_pin_messages?, can_manage_topics?, can_manage_direct_messages?, can_manage_tags?` | `Boolean (True)` | Promotes or demotes a user in a supergroup or channel. | Bot API 3.1 (updated 9.5) |
| [`setChatAdministratorCustomTitle`](https://core.telegram.org/bots/api#setchatadministratorcustomtitle) | `chat_id, user_id, custom_title (0-16 chars, no emoji)` | `Boolean (True)` | Sets a custom title for an administrator promoted by the bot. | Bot API 4.5 |
| [`setChatMemberTag`](https://core.telegram.org/bots/api#setchatmembertag) | `chat_id, user_id, tag? (0-16 chars, no emoji)` | `Boolean (True)` | Sets or removes a custom member tag in a group or supergroup. | Bot API 9.5 |
| [`banChatSenderChat`](https://core.telegram.org/bots/api#banchatsenderchat) | `chat_id, sender_chat_id` | `Boolean (True)` | Bans a channel chat in a supergroup or channel. | Bot API 5.5 |
| [`unbanChatSenderChat`](https://core.telegram.org/bots/api#unbanchatsenderchat) | `chat_id, sender_chat_id` | `Boolean (True)` | Unbans a previously banned channel chat in a supergroup or channel. | Bot API 5.5 |

## Chat Settings & Invite Links (16 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`setChatPermissions`](https://core.telegram.org/bots/api#setchatpermissions) | `chat_id, permissions (ChatPermissions), use_independent_chat_permissions?` | `Boolean (True)` | Sets default chat permissions for all members. | Bot API 4.4 (updated 6.5) |
| [`exportChatInviteLink`](https://core.telegram.org/bots/api#exportchatinvitelink) | `chat_id` | `String (URL)` | Generates a new primary invite link for a chat (revoking the previous primary link). | Bot API 3.1 |
| [`createChatInviteLink`](https://core.telegram.org/bots/api#createchatinvitelink) | `chat_id, name? (0-32), expire_date?, member_limit? (1-99999), creates_join_request?` | `ChatInviteLink` | Creates an additional invite link for a chat. | Bot API 5.1 (updated 5.4) |
| [`editChatInviteLink`](https://core.telegram.org/bots/api#editchatinvitelink) | `chat_id, invite_link, name?, expire_date?, member_limit?, creates_join_request?` | `ChatInviteLink` | Edits a non-primary invite link created by the bot. | Bot API 5.1 (updated 5.4) |
| [`createChatSubscriptionInviteLink`](https://core.telegram.org/bots/api#createchatsubscriptioninvitelink) | `chat_id, subscription_period (2592000 = 30 days), subscription_price (1-10000 Stars), name? (0-32)` | `ChatInviteLink` | Creates a paid Telegram Stars subscription invite link for a channel chat. | Bot API 7.9 |
| [`editChatSubscriptionInviteLink`](https://core.telegram.org/bots/api#editchatsubscriptioninvitelink) | `chat_id, invite_link, name? (0-32)` | `ChatInviteLink` | Edits the name of a subscription invite link created by the bot. | Bot API 7.9 |
| [`revokeChatInviteLink`](https://core.telegram.org/bots/api#revokechatinvitelink) | `chat_id, invite_link` | `ChatInviteLink` | Revokes an invite link created by the bot. | Bot API 5.1 |
| [`approveChatJoinRequest`](https://core.telegram.org/bots/api#approvechatjoinrequest) | `chat_id, user_id` | `Boolean (True)` | Approves a chat join request. | Bot API 5.4 |
| [`declineChatJoinRequest`](https://core.telegram.org/bots/api#declinechatjoinrequest) | `chat_id, user_id` | `Boolean (True)` | Declines a chat join request. | Bot API 5.4 |
| [`setChatPhoto`](https://core.telegram.org/bots/api#setchatphoto) | `chat_id, photo (InputFile)` | `Boolean (True)` | Sets a new profile photo for the chat. | Bot API 3.1 |
| [`deleteChatPhoto`](https://core.telegram.org/bots/api#deletechatphoto) | `chat_id` | `Boolean (True)` | Deletes a chat photo. | Bot API 3.1 |
| [`setChatTitle`](https://core.telegram.org/bots/api#setchattitle) | `chat_id, title (1-128 chars)` | `Boolean (True)` | Changes the title of a chat. | Bot API 3.1 |
| [`setChatDescription`](https://core.telegram.org/bots/api#setchatdescription) | `chat_id, description? (0-255 chars)` | `Boolean (True)` | Changes the description of a group, supergroup, or channel. | Bot API 3.1 |
| [`pinChatMessage`](https://core.telegram.org/bots/api#pinchatmessage) | `chat_id, message_id, business_connection_id?, disable_notification?` | `Boolean (True)` | Adds a message to the list of pinned messages in a chat or business conversation. | Bot API 3.1 (updated 7.4) |
| [`unpinChatMessage`](https://core.telegram.org/bots/api#unpinchatmessage) | `chat_id, business_connection_id?, message_id?` | `Boolean (True)` | Removes a message from the list of pinned messages in a chat. | Bot API 3.1 (updated 7.4) |
| [`unpinAllChatMessages`](https://core.telegram.org/bots/api#unpinallchatmessages) | `chat_id` | `Boolean (True)` | Clears the list of pinned messages in a chat. | Bot API 5.0 |

## Chat Info & Queries (8 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`leaveChat`](https://core.telegram.org/bots/api#leavechat) | `chat_id` | `Boolean (True)` | Use this method for your bot to leave a group, supergroup, or channel. | Bot API 1.0 |
| [`getChat`](https://core.telegram.org/bots/api#getchat) | `chat_id` | `ChatFullInfo` | Returns up-to-date ChatFullInfo about the chat (up to 9999 member IDs on local Bot API server in 10.2+). | Bot API 2.1 (updated 10.4) |
| [`getChatAdministrators`](https://core.telegram.org/bots/api#getchatadministrators) | `chat_id` | `Array of ChatMember` | Returns a list of administrators in a non-private chat. | Bot API 2.1 |
| [`getChatMemberCount`](https://core.telegram.org/bots/api#getchatmembercount) | `chat_id` | `Integer` | Returns the number of members in a chat. | Bot API 5.3 |
| [`getChatMember`](https://core.telegram.org/bots/api#getchatmember) | `chat_id, user_id` | `ChatMember` | Returns information about a member of a chat. | Bot API 2.1 |
| [`getChatShareThemeBackdrops`](https://core.telegram.org/bots/api#getchatsharethemebackdrops) | `None` | `Array of ChatShareThemeBackdrop` | Returns available backdrop styles for custom chat share themes. | Bot API 10.4 |
| [`setChatStickerSet`](https://core.telegram.org/bots/api#setchatstickerset) | `chat_id, sticker_set_name` | `Boolean (True)` | Sets a new group sticker set for a supergroup. | Bot API 3.4 |
| [`deleteChatStickerSet`](https://core.telegram.org/bots/api#deletechatstickerset) | `chat_id` | `Boolean (True)` | Deletes a group sticker set from a supergroup. | Bot API 3.4 |

## Forum Topics (13 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`getForumTopicIconStickers`](https://core.telegram.org/bots/api#getforumtopiciconstickers) | `None` | `Array of Sticker` | Returns custom emoji stickers that can be used as forum topic icons by any user. | Bot API 6.3 |
| [`createForumTopic`](https://core.telegram.org/bots/api#createforumtopic) | `chat_id, name (1-128 chars), icon_color?, icon_custom_emoji_id?` | `ForumTopic` | Creates a topic in a forum supergroup chat or a private chat with a user. | Bot API 6.3 (updated 9.3) |
| [`editForumTopic`](https://core.telegram.org/bots/api#editforumtopic) | `chat_id, message_thread_id, name? (0-128), icon_custom_emoji_id?` | `Boolean (True)` | Edits name and icon of a topic in a forum supergroup or private chat. | Bot API 6.3 (updated 9.3) |
| [`closeForumTopic`](https://core.telegram.org/bots/api#closeforumtopic) | `chat_id, message_thread_id` | `Boolean (True)` | Closes an open topic in a forum supergroup chat. | Bot API 6.3 |
| [`reopenForumTopic`](https://core.telegram.org/bots/api#reopenforumtopic) | `chat_id, message_thread_id` | `Boolean (True)` | Reopens a closed topic in a forum supergroup chat. | Bot API 6.3 |
| [`deleteForumTopic`](https://core.telegram.org/bots/api#deleteforumtopic) | `chat_id, message_thread_id` | `Boolean (True)` | Deletes a forum topic along with all its messages in a forum supergroup or private chat. | Bot API 6.3 (updated 9.3) |
| [`unpinAllForumTopicMessages`](https://core.telegram.org/bots/api#unpinallforumtopicmessages) | `chat_id, message_thread_id` | `Boolean (True)` | Clears the list of pinned messages in a forum topic. | Bot API 6.3 (updated 9.3) |
| [`editGeneralForumTopic`](https://core.telegram.org/bots/api#editgeneralforumtopic) | `chat_id, name (1-128 chars)` | `Boolean (True)` | Edits the name of the 'General' topic in a forum supergroup chat. | Bot API 6.4 |
| [`closeGeneralForumTopic`](https://core.telegram.org/bots/api#closegeneralforumtopic) | `chat_id` | `Boolean (True)` | Closes an open 'General' topic in a forum supergroup chat. | Bot API 6.4 |
| [`reopenGeneralForumTopic`](https://core.telegram.org/bots/api#reopengeneralforumtopic) | `chat_id` | `Boolean (True)` | Reopens a closed 'General' topic in a forum supergroup chat. | Bot API 6.4 |
| [`hideGeneralForumTopic`](https://core.telegram.org/bots/api#hidegeneralforumtopic) | `chat_id` | `Boolean (True)` | Hides the 'General' topic in a forum supergroup chat. | Bot API 6.4 |
| [`unhideGeneralForumTopic`](https://core.telegram.org/bots/api#unhidegeneralforumtopic) | `chat_id` | `Boolean (True)` | Unhides the 'General' topic in a forum supergroup chat. | Bot API 6.4 |
| [`unpinAllGeneralForumTopicMessages`](https://core.telegram.org/bots/api#unpinallgeneralforumtopicmessages) | `chat_id` | `Boolean (True)` | Clears the list of pinned messages in the 'General' forum topic. | Bot API 6.8 |

## Callbacks, Commands & Boosts (20 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`answerCallbackQuery`](https://core.telegram.org/bots/api#answercallbackquery) | `callback_query_id, text? (0-200 chars), show_alert?, url?, cache_time?, ephemeral_message? (EphemeralMessageParameters)` | `Boolean (True)` | Answers a callback query from an inline keyboard (supports ephemeral_message in 10.3+). | Bot API 2.0 (updated 10.4) |
| [`getUserChatBoosts`](https://core.telegram.org/bots/api#getuserchatboosts) | `chat_id, user_id` | `UserChatBoosts` | Returns the list of boosts added to a chat by a user. | Bot API 7.0 |
| [`getBusinessConnection`](https://core.telegram.org/bots/api#getbusinessconnection) | `business_connection_id` | `BusinessConnection` | Returns information about the connection of the bot with a business account. | Bot API 7.2 |
| [`getManagedBotToken`](https://core.telegram.org/bots/api#getmanagedbottoken) | `user_id` | `String (Token)` | Returns the token of a managed bot created on behalf of a user. | Bot API 9.6 |
| [`replaceManagedBotToken`](https://core.telegram.org/bots/api#replacemanagedbottoken) | `user_id` | `String (Token)` | Revokes the current token of a managed bot and generates a new one. | Bot API 9.6 |
| [`setMyCommands`](https://core.telegram.org/bots/api#setmycommands) | `commands (Array of BotCommand, max 100), scope? (BotCommandScope), language_code?` | `Boolean (True)` | Changes the list of the bot's commands for the given scope and user language. | Bot API 4.7 (updated 5.3) |
| [`deleteMyCommands`](https://core.telegram.org/bots/api#deletemycommands) | `scope? (BotCommandScope), language_code?` | `Boolean (True)` | Deletes the list of the bot's commands for the given scope and user language. | Bot API 5.3 |
| [`getMyCommands`](https://core.telegram.org/bots/api#getmycommands) | `scope? (BotCommandScope), language_code?` | `Array of BotCommand` | Returns the current list of the bot's commands for the given scope and language. | Bot API 4.7 (updated 5.3) |
| [`setMyName`](https://core.telegram.org/bots/api#setmyname) | `name? (0-64 chars), language_code?` | `Boolean (True)` | Changes the bot's display name. | Bot API 6.6 |
| [`getMyName`](https://core.telegram.org/bots/api#getmyname) | `language_code?` | `BotName` | Returns the current bot name for the given user language. | Bot API 6.6 |
| [`setMyDescription`](https://core.telegram.org/bots/api#setmydescription) | `description? (0-512 chars), language_code?` | `Boolean (True)` | Changes the bot's description shown in empty chats with the bot. | Bot API 6.6 |
| [`getMyDescription`](https://core.telegram.org/bots/api#getmydescription) | `language_code?` | `BotDescription` | Returns the current bot description for the given user language. | Bot API 6.6 |
| [`setMyShortDescription`](https://core.telegram.org/bots/api#setmyshortdescription) | `short_description? (0-120 chars), language_code?` | `Boolean (True)` | Changes the bot's short description shown on the profile page and when sharing. | Bot API 6.6 |
| [`getMyShortDescription`](https://core.telegram.org/bots/api#getmyshortdescription) | `language_code?` | `BotShortDescription` | Returns the current bot short description for the given user language. | Bot API 6.6 |
| [`setMyProfilePhoto`](https://core.telegram.org/bots/api#setmyprofilephoto) | `photo (InputProfilePhoto)` | `Boolean (True)` | Changes the profile photo of the bot. | Bot API 9.4 |
| [`removeMyProfilePhoto`](https://core.telegram.org/bots/api#removemyprofilephoto) | `None` | `Boolean (True)` | Removes the profile photo of the bot. | Bot API 9.4 |
| [`setChatMenuButton`](https://core.telegram.org/bots/api#setchatmenubutton) | `chat_id?, menu_button? (MenuButton)` | `Boolean (True)` | Changes the bot's menu button in a private chat, or the default menu button. | Bot API 6.0 |
| [`getChatMenuButton`](https://core.telegram.org/bots/api#getchatmenubutton) | `chat_id?` | `MenuButton` | Returns the current value of the bot's menu button in a private chat or default. | Bot API 6.0 |
| [`setMyDefaultAdministratorRights`](https://core.telegram.org/bots/api#setmydefaultadministratorrights) | `rights? (ChatAdministratorRights), for_channels?` | `Boolean (True)` | Changes the default administrator rights requested by the bot when added to groups or channels. | Bot API 6.0 |
| [`getMyDefaultAdministratorRights`](https://core.telegram.org/bots/api#getmydefaultadministratorrights) | `for_channels?` | `ChatAdministratorRights` | Returns the current default administrator rights of the bot. | Bot API 6.0 |

## Gifts, Business & Stories (29 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`getAvailableGifts`](https://core.telegram.org/bots/api#getavailablegifts) | `None` | `Gifts` | Returns the list of gifts that can be sent by the bot to users and channel chats. | Bot API 8.0 |
| [`getUniqueGift`](https://core.telegram.org/bots/api#getuniquegift) | `name (unique gift slug/name)` | `UniqueGiftInfo` | Returns information about a unique collectible gift by its name. | Bot API 10.4 |
| [`sendGift`](https://core.telegram.org/bots/api#sendgift) | `gift_id, user_id?, chat_id?, pay_for_upgrade?, text? (0-128), text_parse_mode?, text_entities?` | `Boolean (True)` | Sends a gift to the given user or channel chat paid from the bot's Star balance. | Bot API 8.0 (updated 8.3) |
| [`giftPremiumSubscription`](https://core.telegram.org/bots/api#giftpremiumsubscription) | `user_id, month_count (3|6|12), star_count (1000|1500|2500), text? (0-128), text_parse_mode?, text_entities?` | `Boolean (True)` | Gifts a Telegram Premium subscription to a user paid in Telegram Stars. | Bot API 9.0 |
| [`verifyUser`](https://core.telegram.org/bots/api#verifyuser) | `user_id, custom_description? (0-70 chars)` | `Boolean (True)` | Verifies a user on behalf of the organization represented by the bot. | Bot API 8.2 |
| [`verifyChat`](https://core.telegram.org/bots/api#verifychat) | `chat_id, custom_description? (0-70 chars)` | `Boolean (True)` | Verifies a chat on behalf of the organization represented by the bot. | Bot API 8.2 |
| [`removeUserVerification`](https://core.telegram.org/bots/api#removeuserverification) | `user_id` | `Boolean (True)` | Removes verification from a user who is currently verified on behalf of the organization. | Bot API 8.2 |
| [`removeChatVerification`](https://core.telegram.org/bots/api#removechatverification) | `chat_id` | `Boolean (True)` | Removes verification from a chat that is currently verified on behalf of the organization. | Bot API 8.2 |
| [`readBusinessMessage`](https://core.telegram.org/bots/api#readbusinessmessage) | `business_connection_id, chat_id, message_id` | `Boolean (True)` | Marks an incoming message as read on behalf of a business account. | Bot API 9.0 |
| [`deleteBusinessMessages`](https://core.telegram.org/bots/api#deletebusinessmessages) | `business_connection_id, message_ids (1-100 IDs)` | `Boolean (True)` | Deletes messages on behalf of a business account. | Bot API 9.0 |
| [`setBusinessAccountName`](https://core.telegram.org/bots/api#setbusinessaccountname) | `business_connection_id, first_name (1-64), last_name? (0-64)` | `Boolean (True)` | Changes the first and last name of a managed business account. | Bot API 9.0 |
| [`setBusinessAccountUsername`](https://core.telegram.org/bots/api#setbusinessaccountusername) | `business_connection_id, username? (0-32)` | `Boolean (True)` | Changes the username of a managed business account. | Bot API 9.0 |
| [`setBusinessAccountBio`](https://core.telegram.org/bots/api#setbusinessaccountbio) | `business_connection_id, bio? (0-140)` | `Boolean (True)` | Changes the bio of a managed business account. | Bot API 9.0 |
| [`setBusinessAccountProfilePhoto`](https://core.telegram.org/bots/api#setbusinessaccountprofilephoto) | `business_connection_id, photo (InputProfilePhoto), is_public?` | `Boolean (True)` | Changes the profile photo of a managed business account. | Bot API 9.0 |
| [`removeBusinessAccountProfilePhoto`](https://core.telegram.org/bots/api#removebusinessaccountprofilephoto) | `business_connection_id, is_public?` | `Boolean (True)` | Removes the current profile photo of a managed business account. | Bot API 9.0 |
| [`setBusinessAccountGiftSettings`](https://core.telegram.org/bots/api#setbusinessaccountgiftsettings) | `business_connection_id, show_gift_button, accepted_gift_types (AcceptedGiftTypes)` | `Boolean (True)` | Changes the privacy settings pertaining to incoming gifts in a managed business account. | Bot API 9.0 |
| [`getBusinessAccountStarBalance`](https://core.telegram.org/bots/api#getbusinessaccountstarbalance) | `business_connection_id` | `StarAmount` | Returns the amount of Telegram Stars owned by a managed business account. | Bot API 9.0 |
| [`transferBusinessAccountStars`](https://core.telegram.org/bots/api#transferbusinessaccountstars) | `business_connection_id, star_count (1-10000)` | `Boolean (True)` | Transfers Telegram Stars from the business account balance to the bot's balance. | Bot API 9.0 |
| [`getBusinessAccountGifts`](https://core.telegram.org/bots/api#getbusinessaccountgifts) | `business_connection_id, exclude_unsaved?, exclude_saved?, exclude_unlimited?, exclude_limited_upgradable?, exclude_limited_non_upgradable?, exclude_unique?, exclude_from_blockchain?, sort_by_price?, offset?, limit? (1-100)` | `OwnedGifts` | Returns the gifts received and owned by a managed business account. | Bot API 9.0 (updated 9.3) |
| [`getUserGifts`](https://core.telegram.org/bots/api#getusergifts) | `user_id, exclude_unlimited?, exclude_limited_upgradable?, exclude_limited_non_upgradable?, exclude_from_blockchain?, exclude_unique?, sort_by_price?, offset?, limit? (1-100)` | `OwnedGifts` | Returns the gifts owned and hosted by a user. | Bot API 9.3 |
| [`getChatGifts`](https://core.telegram.org/bots/api#getchatgifts) | `chat_id, exclude_unsaved?, exclude_saved?, exclude_unlimited?, exclude_limited_upgradable?, exclude_limited_non_upgradable?, exclude_from_blockchain?, exclude_unique?, sort_by_price?, offset?, limit? (1-100)` | `OwnedGifts` | Returns the gifts owned by a chat. | Bot API 9.3 |
| [`convertGiftToStars`](https://core.telegram.org/bots/api#convertgifttostars) | `business_connection_id, owned_gift_id` | `Boolean (True)` | Converts a given regular gift to Telegram Stars on a business account. | Bot API 9.0 |
| [`upgradeGift`](https://core.telegram.org/bots/api#upgradegift) | `business_connection_id, owned_gift_id, keep_original_details?, star_count?` | `Boolean (True)` | Upgrades a given regular gift to a unique collectible gift. | Bot API 9.0 |
| [`transferGift`](https://core.telegram.org/bots/api#transfergift) | `business_connection_id, owned_gift_id, new_owner_chat_id, star_count?` | `Boolean (True)` | Transfers an owned unique gift to another user. | Bot API 9.0 |
| [`deleteBusinessAccountGift`](https://core.telegram.org/bots/api#deletebusinessaccountgift) | `business_connection_id, owned_gift_id` | `Boolean (True)` | Deletes a regular gift received by a managed business account. | Bot API 10.4 |
| [`postStory`](https://core.telegram.org/bots/api#poststory) | `business_connection_id, content (InputStoryContent), active_period (21600|43200|86400|172800), caption? (0-2048), parse_mode?, caption_entities?, areas? (Array of StoryArea), post_to_chat_page?, protect_content?` | `Story` | Posts a story on behalf of a managed business account. | Bot API 9.0 |
| [`repostStory`](https://core.telegram.org/bots/api#repoststory) | `business_connection_id, from_chat_id, from_story_id, active_period, post_to_chat_page?, protect_content?` | `Story` | Reposts a story across managed business accounts. | Bot API 9.3 |
| [`editStory`](https://core.telegram.org/bots/api#editstory) | `business_connection_id, story_id, content (InputStoryContent), caption?, parse_mode?, caption_entities?, areas?` | `Story` | Edits a story previously posted by the bot on behalf of a managed business account. | Bot API 9.0 |
| [`deleteStory`](https://core.telegram.org/bots/api#deletestory) | `business_connection_id, story_id` | `Boolean (True)` | Deletes a story previously posted by the bot on behalf of a managed business account. | Bot API 9.0 |

## Updating Messages (21 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`editMessageText`](https://core.telegram.org/bots/api#editmessagetext) | `text (1-4096), business_connection_id?, chat_id?, message_id?, inline_message_id?, parse_mode?, entities?, link_preview_options?, reply_markup?` | `Message | Boolean` | Edits text and game messages. | Bot API 2.0 (updated 7.4) |
| [`editMessageCaption`](https://core.telegram.org/bots/api#editmessagecaption) | `business_connection_id?, chat_id?, message_id?, inline_message_id?, caption? (0-1024), parse_mode?, caption_entities?, show_caption_above_media?, reply_markup?` | `Message | Boolean` | Edits captions of messages. | Bot API 2.0 (updated 7.4) |
| [`editMessageMedia`](https://core.telegram.org/bots/api#editmessagemedia) | `media (InputMedia), business_connection_id?, chat_id?, message_id?, inline_message_id?, reply_markup?` | `Message | Boolean` | Edits animation, audio, document, photo, or video messages, or adds media to text messages. | Bot API 4.0 (updated 7.10) |
| [`editMessageLiveLocation`](https://core.telegram.org/bots/api#editmessagelivelocation) | `latitude, longitude, business_connection_id?, chat_id?, message_id?, inline_message_id?, live_period?, horizontal_accuracy?, heading?, proximity_alert_radius?, reply_markup?` | `Message | Boolean` | Edits live location messages. | Bot API 3.4 (updated 7.4) |
| [`stopMessageLiveLocation`](https://core.telegram.org/bots/api#stopmessagelivelocation) | `business_connection_id?, chat_id?, message_id?, inline_message_id?, reply_markup?` | `Message | Boolean` | Stops updating a live location message before live_period expires. | Bot API 3.4 (updated 7.4) |
| [`editMessageChecklist`](https://core.telegram.org/bots/api#editmessagechecklist) | `business_connection_id, chat_id, message_id, checklist (InputChecklist), reply_markup?` | `Message` | Edits a checklist on behalf of a connected business account. | Bot API 9.1 |
| [`editMessageReplyMarkup`](https://core.telegram.org/bots/api#editmessagereplymarkup) | `business_connection_id?, chat_id?, message_id?, inline_message_id?, reply_markup?` | `Message | Boolean` | Edits only the reply markup of messages. | Bot API 2.0 (updated 7.4) |
| [`stopPoll`](https://core.telegram.org/bots/api#stoppoll) | `chat_id, message_id, business_connection_id?, reply_markup?` | `Poll` | Stops a poll which was sent by the bot. | Bot API 4.2 (updated 7.4) |
| [`editMessagePoll`](https://core.telegram.org/bots/api#editmessagepoll) | `chat_id, message_id, poll (InputPoll), reply_markup?` | `Message` | Edits an active poll sent by the bot. | Bot API 10.1 |
| [`addMessagePollOption`](https://core.telegram.org/bots/api#addmessagepolloption) | `chat_id, message_id, option (InputPollOption)` | `Boolean (True)` | Adds a new option to an active poll that allows adding options. | Bot API 10.1 |
| [`deleteMessagePollOption`](https://core.telegram.org/bots/api#deletemessagepolloption) | `chat_id, message_id, option_persistent_id` | `Boolean (True)` | Deletes an option from an active poll by its persistent_id. | Bot API 10.1 |
| [`editMessageWidgetData`](https://core.telegram.org/bots/api#editmessagewidgetdata) | `data (0-4096 chars), chat_id?, message_id?, inline_message_id?, receiver_user_id?` | `Boolean (True)` | Updates the data string of an in-chat Widget (per-user if receiver_user_id is specified). | Bot API 10.4 |
| [`editSharedWidgetData`](https://core.telegram.org/bots/api#editsharedwidgetdata) | `data (0-4096 chars), chat_id?, message_id?, inline_message_id?` | `Boolean (True)` | Updates the shared state data of an in-chat SharedWidget for all chat participants. | Bot API 10.4 |
| [`approveSuggestedPost`](https://core.telegram.org/bots/api#approvesuggestedpost) | `chat_id, message_id, send_date?` | `Boolean (True)` | Approves an incoming suggested post in a direct messages chat. | Bot API 9.2 |
| [`declineSuggestedPost`](https://core.telegram.org/bots/api#declinesuggestedpost) | `chat_id, message_id, comment?` | `Boolean (True)` | Declines an incoming suggested post in a direct messages chat. | Bot API 9.2 |
| [`deleteMessage`](https://core.telegram.org/bots/api#deletemessage) | `chat_id, message_id` | `Boolean (True)` | Deletes a message, including service messages (subject to 48-hour and permission rules). | Bot API 3.0 |
| [`deleteMessages`](https://core.telegram.org/bots/api#deletemessages) | `chat_id, message_ids (1-100 IDs)` | `Boolean (True)` | Deletes up to 100 messages simultaneously. | Bot API 7.0 |
| [`sendChatMessageDraft`](https://core.telegram.org/bots/api#sendchatmessagedraft) | `chat_id, text? (0-4096), message_thread_id?, direct_messages_topic_id?, parse_mode?, entities?, link_preview_options?, reply_parameters?` | `Boolean (True)` | Sets or clears the input field message draft in a chat. | Bot API 10.2 |
| [`setChatMessageAutoDeleteTime`](https://core.telegram.org/bots/api#setchatmessageautodeletetime) | `chat_id, message_auto_delete_time (0 or seconds)` | `Boolean (True)` | Changes the message auto-delete timer in a chat. | Bot API 10.1 |
| [`setChatTranslationLanguage`](https://core.telegram.org/bots/api#setchattranslationlanguage) | `chat_id, language_code?` | `Boolean (True)` | Sets or disables automatic translation language in a channel or supergroup. | Bot API 10.1 |
| [`setChatDirectMessagesPrice`](https://core.telegram.org/bots/api#setchatdirectmessagesprice) | `chat_id, paid_message_star_count (0-10000)` | `Boolean (True)` | Sets the price in Telegram Stars required to send direct messages to a channel monoforum. | Bot API 10.1 |

## Stickers (16 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`sendSticker`](https://core.telegram.org/bots/api#sendsticker) | `chat_id, sticker (InputFile|String), business_connection_id?, message_thread_id?, direct_messages_topic_id?, emoji?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends static .WEBP, animated .TGS, or video .WEBM stickers. | Bot API 1.0 (updated 9.2) |
| [`getStickerSet`](https://core.telegram.org/bots/api#getstickerset) | `name` | `StickerSet` | Returns a StickerSet object by its short name. | Bot API 3.2 |
| [`getCustomEmojiStickers`](https://core.telegram.org/bots/api#getcustomemojistickers) | `custom_emoji_ids (1-200 IDs)` | `Array of Sticker` | Returns information about custom emoji stickers by their identifiers. | Bot API 6.2 |
| [`uploadStickerFile`](https://core.telegram.org/bots/api#uploadstickerfile) | `user_id, sticker (InputFile), sticker_format ('static'|'animated'|'video')` | `File` | Uploads a sticker file for later use in createNewStickerSet / addStickerToSet. | Bot API 3.2 (updated 6.6) |
| [`createNewStickerSet`](https://core.telegram.org/bots/api#createnewstickerset) | `user_id, name (1-64 chars ending in _by_<bot_username>), title (1-64), stickers (1-50 InputSticker), sticker_type? ('regular'|'mask'|'custom_emoji'), needs_repainting?` | `Boolean (True)` | Creates a new sticker set owned by a user. | Bot API 3.2 (updated 7.2) |
| [`addStickerToSet`](https://core.telegram.org/bots/api#addstickertoset) | `user_id, name, sticker (InputSticker)` | `Boolean (True)` | Adds a new sticker to a set created by the bot (max 200 custom emoji or 120 regular stickers). | Bot API 3.2 (updated 6.6) |
| [`setStickerPositionInSet`](https://core.telegram.org/bots/api#setstickerpositioninset) | `sticker (file_id), position (0-based)` | `Boolean (True)` | Moves a sticker in a set created by the bot to a specific position. | Bot API 3.2 |
| [`deleteStickerFromSet`](https://core.telegram.org/bots/api#deletestickerfromset) | `sticker (file_id)` | `Boolean (True)` | Deletes a sticker from a set created by the bot. | Bot API 3.2 |
| [`replaceStickerInSet`](https://core.telegram.org/bots/api#replacestickerinset) | `user_id, name, old_sticker (file_id), sticker (InputSticker)` | `Boolean (True)` | Replaces an existing sticker in a sticker set with a new one. | Bot API 7.2 |
| [`setStickerEmojiList`](https://core.telegram.org/bots/api#setstickeremojilist) | `sticker (file_id), emoji_list (1-20 emojis)` | `Boolean (True)` | Changes the list of 1-20 emojis assigned to a regular or custom emoji sticker. | Bot API 6.6 |
| [`setStickerKeywords`](https://core.telegram.org/bots/api#setstickerkeywords) | `sticker (file_id), keywords? (0-20 strings of 0-64 chars)` | `Boolean (True)` | Changes search keywords assigned to a regular or custom emoji sticker. | Bot API 6.6 |
| [`setStickerMaskPosition`](https://core.telegram.org/bots/api#setstickermaskposition) | `sticker (file_id), mask_position? (MaskPosition)` | `Boolean (True)` | Changes the mask position of a mask sticker. | Bot API 6.6 |
| [`setStickerSetTitle`](https://core.telegram.org/bots/api#setstickersettitle) | `name, title (1-64 chars)` | `Boolean (True)` | Sets the title of a created sticker set. | Bot API 6.6 |
| [`setStickerSetThumbnail`](https://core.telegram.org/bots/api#setstickersetthumbnail) | `name, user_id, format ('static'|'animated'|'video'), thumbnail? (InputFile|String)` | `Boolean (True)` | Sets the thumbnail of a regular or mask sticker set. | Bot API 4.7 (updated 6.6) |
| [`setCustomEmojiStickerSetThumbnail`](https://core.telegram.org/bots/api#setcustomemojistickersetthumbnail) | `name, custom_emoji_id?` | `Boolean (True)` | Sets the thumbnail of a custom emoji sticker set. | Bot API 6.6 |
| [`deleteStickerSet`](https://core.telegram.org/bots/api#deletestickerset) | `name` | `Boolean (True)` | Deletes a sticker set that was created by the bot. | Bot API 6.6 |

## Rich Messages (2 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`sendRichMessage`](https://core.telegram.org/bots/api#sendrichmessage) | `chat_id, message (InputRichMessage), business_connection_id?, message_thread_id?, direct_messages_topic_id?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends a structured multi-block RichMessage (headers, tables, code blocks, collapsibles, media). | Bot API 10.2 |
| [`sendRichMessageDraft`](https://core.telegram.org/bots/api#sendrichmessagedraft) | `chat_id, draft_id (non-zero int), message (InputRichMessage), message_thread_id?` | `Boolean (True)` | Streams a partial structured RichMessage draft to a user. | Bot API 10.2 |

## Inline Mode (3 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`answerInlineQuery`](https://core.telegram.org/bots/api#answerinlinequery) | `inline_query_id, results (Array of InlineQueryResult, max 50), cache_time? (default 300s), is_personal?, next_offset? (max 64B), button? (InlineQueryResultsButton)` | `Boolean (True)` | Sends answers (up to 50 results) to an inline query. | Bot API 1.0 (updated 6.7) |
| [`answerWebAppQuery`](https://core.telegram.org/bots/api#answerwebappquery) | `web_app_query_id, result (InlineQueryResult)` | `SentWebAppMessage` | Sets the result of an interaction with a Mini App and sends a message on behalf of the user. | Bot API 6.0 |
| [`savePreparedInlineMessage`](https://core.telegram.org/bots/api#savepreparedinlinemessage) | `user_id, result (InlineQueryResult), allow_user_chats?, allow_bot_chats?, allow_group_chats?, allow_channel_chats?` | `PreparedInlineMessage` | Stores a message that can be sent by a Mini App via Telegram.WebApp.shareMessage(id). | Bot API 8.0 |

## Payments & Stars (8 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`sendInvoice`](https://core.telegram.org/bots/api#sendinvoice) | `chat_id, title (1-32), description (1-255), payload (1-128B), currency ('XTR' or ISO 4217), prices (Array of LabeledPrice), message_thread_id?, direct_messages_topic_id?, provider_token? (empty for XTR), max_tip_amount?, suggested_tip_amounts?, start_parameter?, provider_data?, photo_url?, photo_size?, photo_width?, photo_height?, need_name?, need_phone_number?, need_email?, need_shipping_address?, send_phone_number_to_provider?, send_email_to_provider?, is_flexible?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, suggested_post_parameters?, reply_parameters?, reply_markup?` | `Message` | Sends an invoice to a chat (for Telegram Stars, set currency='XTR' and omit provider_token). | Bot API 3.0 (updated 9.2) |
| [`createInvoiceLink`](https://core.telegram.org/bots/api#createinvoicelink) | `title (1-32), description (1-255), payload (1-128B), currency ('XTR' or ISO 4217), prices (Array of LabeledPrice), business_connection_id?, provider_token?, subscription_period? (2592000 for 30d XTR subscription), max_tip_amount?, suggested_tip_amounts?, provider_data?, photo_url?, photo_size?, photo_width?, photo_height?, need_name?, need_phone_number?, need_email?, need_shipping_address?, send_phone_number_to_provider?, send_email_to_provider?, is_flexible?` | `String (URL)` | Creates a shareable link for an invoice or recurring 30-day Telegram Stars subscription. | Bot API 6.1 (updated 8.0) |
| [`answerShippingQuery`](https://core.telegram.org/bots/api#answershippingquery) | `shipping_query_id, ok, shipping_options? (Array of ShippingOption), error_message?` | `Boolean (True)` | Replies to shipping queries when an invoice has is_flexible=True. | Bot API 3.0 |
| [`answerPreCheckoutQuery`](https://core.telegram.org/bots/api#answerprecheckoutquery) | `pre_checkout_query_id, ok, error_message?` | `Boolean (True)` | Confirms final checkout within 10 seconds of receiving pre_checkout_query. | Bot API 3.0 |
| [`getMyStarBalance`](https://core.telegram.org/bots/api#getmystarbalance) | `None` | `StarAmount` | Returns the current balance of Telegram Stars owned by the bot. | Bot API 9.1 |
| [`getStarTransactions`](https://core.telegram.org/bots/api#getstartransactions) | `offset?, limit? (1-100)` | `StarTransactions` | Returns the bot's Telegram Star transactions in chronological order. | Bot API 7.4 |
| [`refundStarPayment`](https://core.telegram.org/bots/api#refundstarpayment) | `user_id, telegram_payment_charge_id` | `Boolean (True)` | Refunds a successful payment in Telegram Stars. | Bot API 7.4 |
| [`editUserStarSubscription`](https://core.telegram.org/bots/api#edituserstarsubscription) | `user_id, telegram_payment_charge_id, is_canceled` | `Boolean (True)` | Allows the bot to cancel or re-enable extension of a recurring Telegram Star subscription. | Bot API 8.0 |

## Telegram Passport (1 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`setPassportDataErrors`](https://core.telegram.org/bots/api#setpassportdataerrors) | `user_id, errors (Array of PassportElementError)` | `Boolean (True)` | Informs a user that some of the Telegram Passport elements they provided contain errors. | Bot API 4.0 |

## Games (3 Methods)

| Method | Parameters (`?` = optional) | Returns | Purpose & Limits | Version |
|---|---|---|---|---|
| [`sendGame`](https://core.telegram.org/bots/api#sendgame) | `chat_id, game_short_name, business_connection_id?, message_thread_id?, disable_notification?, protect_content?, allow_paid_broadcast?, message_effect_id?, reply_parameters?, reply_markup?` | `Message` | Sends an HTML5 game registered via @BotFather. | Bot API 2.2 (updated 7.4) |
| [`setGameScore`](https://core.telegram.org/bots/api#setgamescore) | `user_id, score (non-negative int), force?, disable_edit_message?, chat_id?, message_id?, inline_message_id?` | `Message | Boolean` | Sets the score of the specified user in a game message. | Bot API 2.2 |
| [`getGameHighScores`](https://core.telegram.org/bots/api#getgamehighscores) | `user_id, chat_id?, message_id?, inline_message_id?` | `Array of GameHighScore` | Returns data for high score tables around the target user. | Bot API 2.2 |

---

## Minimal Working Examples by Category

### 1. Sending a Message with Link Preview & Reply Parameters (`sendMessage`)
```json
{
  "method": "sendMessage",
  "chat_id": -1001234567890,
  "text": "<b>Release 10.4 is live!</b> Check out <a href=\"https://core.telegram.org/bots/widgets\">In-Chat Widgets</a>.",
  "parse_mode": "HTML",
  "link_preview_options": {
    "is_disabled": false,
    "prefer_small_media": true,
    "show_above_text": false
  },
  "reply_parameters": {
    "message_id": 42,
    "allow_sending_without_reply": true
  }
}
```

### 2. Sending an In-Chat Interactive HTML Widget (`sendWidget`, Bot API 10.4)
```json
{
  "method": "sendWidget",
  "chat_id": 123456789,
  "url": "https://widgets.example.com/live-order-tracker",
  "aspect_ratio": "16:9",
  "data": "{\"order_id\":\"ORD-901\",\"step\":2}"
}
```

### 3. Answering a Callback Query with an Ephemeral Message (`answerCallbackQuery`, Bot API 10.3 / 10.4)
```json
{
  "method": "answerCallbackQuery",
  "callback_query_id": "4382910492819201",
  "ephemeral_message": {
    "text": "✅ Your private verification code is <code>849201</code> (visible only to you).",
    "parse_mode": "HTML"
  }
}
```

### 4. Sending a Structured Multi-Block Rich Message (`sendRichMessage`, Bot API 10.2 / 10.4)
```json
{
  "method": "sendRichMessage",
  "chat_id": 123456789,
  "message": {
    "blocks": [
      {
        "type": "header",
        "text": { "type": "plain", "text": "Deployment Summary" }
      },
      {
        "type": "paragraph",
        "text": {
          "type": "concat",
          "texts": [
            { "type": "bold", "text": { "type": "plain", "text": "TON Payout Address: " } },
            { "type": "ton_address", "text": { "type": "plain", "text": "UQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqEBI" } }
          ]
        }
      }
    ]
  }
}
```
