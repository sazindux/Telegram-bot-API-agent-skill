# Telegram Bot API 10.4 — Complete Types Catalog (402 Types)

- **Verified Against:** Bot API 10.4 (November 9, 2026)
- **Verification Date:** November 11, 2026
- **Primary Source:** [Telegram Bot API Specification](https://core.telegram.org/bots/api)
- **Changelog Source:** [Bot API Changelog](https://core.telegram.org/bots/api-changelog)

This file catalogs all **402 objects and union types** in Bot API 10.4 (the complete documented surface of the official specification, including all `RichText*` / `RichBlock*` Rich Message sub-types and every union type), grouped by domain with direct links to `https://core.telegram.org/bots/api#<type>`.

---

## Getting Updates (2)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`Update`](https://core.telegram.org/bots/api#update) | Incoming event envelope (update_id + at most 1 optional field: message, edited_message, channel_post, edited_channel_post, business_connection, business_message, edited_business_message, deleted_business_messages, message_reaction, message_reaction_count, inline_query, chosen_inline_result, callback_query, shipping_query, pre_checkout_query, purchased_paid_media, poll, poll_answer, my_chat_member, chat_member, chat_join_request, chat_boost, removed_chat_boost, managed_bot, widget_query, shared_widget_query). | Bot API 1.0 (updated 10.4) |
| [`WebhookInfo`](https://core.telegram.org/bots/api#webhookinfo) | Describes the current status of a webhook (url, has_custom_certificate, pending_update_count, ip_address, last_error_date, last_error_message, last_synchronization_error_date, max_connections, allowed_updates). | Bot API 2.1 |

## Core Users, Chats & Messages (30)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`User`](https://core.telegram.org/bots/api#user) | Represents a Telegram user or bot (id, is_bot, first_name, last_name, username, language_code, is_premium, added_to_attachment_menu, can_join_groups, can_read_all_group_messages, supports_inline_queries, can_connect_to_business, has_main_web_app, has_topics_enabled, allows_users_to_create_topics, can_manage_bots). | Bot API 1.0 (updated 9.6) |
| [`Chat`](https://core.telegram.org/bots/api#chat) | Represents a chat (id, type: 'private'|'group'|'supergroup'|'channel', title, username, first_name, last_name, is_forum, is_direct_messages). | Bot API 1.0 (updated 9.1) |
| [`ChatFullInfo`](https://core.telegram.org/bots/api#chatfullinfo) | Complete metadata about a chat returned by getChat (accent_color_id, max_reaction_count, photo, active_usernames, birthdate, business_intro, business_location, business_opening_hours, personal_chat, parent_chat, available_reactions, background_custom_emoji_id, profile_accent_color_id, profile_background_custom_emoji_id, emoji_status_custom_emoji_id, emoji_status_expiration_date, bio, has_private_forwards, has_restricted_voice_and_video_messages, join_to_send_messages, join_by_request, description, invite_link, pinned_message, permissions, accepted_gift_types, can_send_paid_media, slow_mode_delay, unrestrict_boost_count, message_auto_delete_time, has_aggressive_anti_spam_enabled, has_hidden_members, has_protected_content, has_visible_history, sticker_set_name, can_set_sticker_set, custom_emoji_sticker_set_name, linked_chat_id, location, rating, first_profile_audio, unique_gift_colors, paid_message_star_count, share_theme, member_ids). | Bot API 7.3 (updated 10.4) |
| [`Message`](https://core.telegram.org/bots/api#message) | Represents a message in a chat (includes widget, shared_widget, paid_messages_waived, rich_message, checklist, suggested_post_info, paid_star_count, direct_messages_topic, sender_tag, etc.). | Bot API 1.0 (updated 10.4) |
| [`MessageId`](https://core.telegram.org/bots/api#messageid) | Represents a unique message identifier (message_id). | Bot API 5.0 |
| [`InaccessibleMessage`](https://core.telegram.org/bots/api#inaccessiblemessage) | Describes a message that was deleted or is otherwise inaccessible to the bot (chat, message_id, date=0). | Bot API 7.0 |
| [`MaybeInaccessibleMessage`](https://core.telegram.org/bots/api#maybeinaccessiblemessage) | Union of Message | InaccessibleMessage. | Bot API 7.0 |
| [`MessageEntity`](https://core.telegram.org/bots/api#messageentity) | Represents one special entity in a text message (type: mention, hashtag, cashtag, bot_command, url, email, phone_number, bold, italic, underline, strikethrough, spoiler, blockquote, expandable_blockquote, code, pre, text_link, text_mention, custom_emoji, date_time, ton_address, bank_card_number; offset and length in UTF-16 code units). | Bot API 1.0 (updated 10.4) |
| [`TextQuote`](https://core.telegram.org/bots/api#textquote) | Contains information about the quoted part of a message that is replied to (text, entities, position, is_manual). | Bot API 7.0 |
| [`ExternalReplyInfo`](https://core.telegram.org/bots/api#externalreplyinfo) | Contains information about a message that is being replied to, which may come from another chat or forum topic. | Bot API 7.0 (updated 10.4) |
| [`ReplyParameters`](https://core.telegram.org/bots/api#replyparameters) | Describes reply parameters for the message that is being sent (message_id, chat_id, allow_sending_without_reply, quote, quote_parse_mode, quote_entities, quote_position, checklist_task_id, poll_option_id). | Bot API 7.0 (updated 10.1) |
| [`MessageOrigin`](https://core.telegram.org/bots/api#messageorigin) | Union describing the origin of a forwarded message (MessageOriginUser | MessageOriginHiddenUser | MessageOriginChat | MessageOriginChannel). | Bot API 7.0 |
| [`MessageOriginUser`](https://core.telegram.org/bots/api#messageoriginuser) | The message was originally sent by a known user. | Bot API 7.0 |
| [`MessageOriginHiddenUser`](https://core.telegram.org/bots/api#messageoriginhiddenuser) | The message was originally sent by an unknown user. | Bot API 7.0 |
| [`MessageOriginChat`](https://core.telegram.org/bots/api#messageoriginchat) | The message was originally sent on behalf of a chat to a group chat. | Bot API 7.0 |
| [`MessageOriginChannel`](https://core.telegram.org/bots/api#messageoriginchannel) | The message was originally sent to a channel chat. | Bot API 7.0 |
| [`LinkPreviewOptions`](https://core.telegram.org/bots/api#linkpreviewoptions) | Describes the options used for link preview generation (is_disabled, url, prefer_small_media, prefer_large_media, show_above_text). | Bot API 7.0 |
| [`EphemeralMessageParameters`](https://core.telegram.org/bots/api#ephemeralmessageparameters) | Parameters for sending a temporary client-side ephemeral message (text, parse_mode, entities, link_preview_options, reply_markup). | Bot API 10.3 |
| [`DirectMessagesTopic`](https://core.telegram.org/bots/api#directmessagestopic) | Describes a topic in a direct messages chat (Monoforum): topic_id, user. | Bot API 9.1 |
| [`PaidMessagesWaived`](https://core.telegram.org/bots/api#paidmessageswaived) | Service message: the price for paid messages was waived for a user in a direct messages chat. | Bot API 10.4 |
| [`PaidMessagePriceChanged`](https://core.telegram.org/bots/api#paidmessagepricechanged) | Service message: the price for paid messages has changed in the chat. | Bot API 9.0 |
| [`DirectMessagePriceChanged`](https://core.telegram.org/bots/api#directmessagepricechanged) | Service message: the price for direct messages in a channel monoforum has changed. | Bot API 9.1 |
| [`MessageAutoDeleteTimerChanged`](https://core.telegram.org/bots/api#messageautodeletetimerchanged) | Service message: auto-delete timer settings changed. | Bot API 5.1 |
| [`ChatBoostAdded`](https://core.telegram.org/bots/api#chatboostadded) | Service message: user boosted the chat. | Bot API 7.1 |
| [`UsersShared`](https://core.telegram.org/bots/api#usersshared) | Service message: users were shared with the bot via KeyboardButtonRequestUsers. | Bot API 7.0 |
| [`ChatShared`](https://core.telegram.org/bots/api#chatshared) | Service message: a chat was shared with the bot via KeyboardButtonRequestChat. | Bot API 6.5 (updated 7.0) |
| [`WriteAccessAllowed`](https://core.telegram.org/bots/api#writeaccessallowed) | Service message: user allowed the bot to write messages after launching a Web App, connecting a website, or adding to attachment menu. | Bot API 6.4 (updated 6.6) |
| [`ManagedBotCreated`](https://core.telegram.org/bots/api#managedbotcreated) | Service message: a managed bot was created by a user via KeyboardButtonRequestManagedBot. | Bot API 9.6 |
| [`ManagedBotUpdated`](https://core.telegram.org/bots/api#managedbotupdated) | Update payload when a managed bot is created or its token is updated. | Bot API 9.6 |
| [`ResponseParameters`](https://core.telegram.org/bots/api#responseparameters) | Describes why a request was unsuccessful (migrate_to_chat_id, retry_after). | Bot API 2.1 |

## Media, Files, Polls & Checklists (38)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`PhotoSize`](https://core.telegram.org/bots/api#photosize) | Represents one size of a photo or a file / sticker thumbnail. | Bot API 1.0 |
| [`Animation`](https://core.telegram.org/bots/api#animation) | Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound). | Bot API 4.0 |
| [`Audio`](https://core.telegram.org/bots/api#audio) | Represents an audio file to be treated as music by the Telegram clients. | Bot API 1.0 |
| [`Document`](https://core.telegram.org/bots/api#document) | Represents a general file. | Bot API 1.0 |
| [`Story`](https://core.telegram.org/bots/api#story) | Represents a story (chat, id). | Bot API 7.0 |
| [`VideoQuality`](https://core.telegram.org/bots/api#videoquality) | Represents a specific resolution/codec variant of a Video (file_id, file_unique_id, width, height, codec, file_size). | Bot API 9.5 |
| [`Video`](https://core.telegram.org/bots/api#video) | Represents a video file (includes cover, start_timestamp, qualities). | Bot API 1.0 (updated 9.5) |
| [`VideoNote`](https://core.telegram.org/bots/api#videonote) | Represents a rounded video message. | Bot API 3.0 |
| [`Voice`](https://core.telegram.org/bots/api#voice) | Represents a voice note. | Bot API 1.0 |
| [`PaidMediaInfo`](https://core.telegram.org/bots/api#paidmediainfo) | Describes the paid media added to a message (star_count, paid_media). | Bot API 7.6 |
| [`PaidMedia`](https://core.telegram.org/bots/api#paidmedia) | Union of PaidMediaPreview | PaidMediaPhoto | PaidMediaVideo. | Bot API 7.6 |
| [`PaidMediaPreview`](https://core.telegram.org/bots/api#paidmediapreview) | The paid media isn't available before the payment. | Bot API 7.6 |
| [`PaidMediaPhoto`](https://core.telegram.org/bots/api#paidmediaphoto) | The paid media is a photo. | Bot API 7.6 |
| [`PaidMediaVideo`](https://core.telegram.org/bots/api#paidmediavideo) | The paid media is a video. | Bot API 7.6 |
| [`Contact`](https://core.telegram.org/bots/api#contact) | Represents a phone contact. | Bot API 1.0 |
| [`Dice`](https://core.telegram.org/bots/api#dice) | Represents an animated emoji that displays a random value. | Bot API 4.7 |
| [`PollOption`](https://core.telegram.org/bots/api#polloption) | Contains information about one answer option in a poll (persistent_id, text, text_entities, voter_count, added_by_user, added_by_chat, addition_date). | Bot API 4.2 (updated 10.1) |
| [`InputPollOption`](https://core.telegram.org/bots/api#inputpolloption) | Contains information about one answer option in a poll to be sent (text, text_parse_mode, text_entities). | Bot API 7.3 |
| [`InputPoll`](https://core.telegram.org/bots/api#inputpoll) | Describes a poll to be edited via editMessagePoll. | Bot API 10.1 |
| [`PollAnswer`](https://core.telegram.org/bots/api#pollanswer) | Represents an answer of a user in a non-anonymous poll (poll_id, voter_chat, user, option_ids, option_persistent_ids). | Bot API 4.5 (updated 10.1) |
| [`Poll`](https://core.telegram.org/bots/api#poll) | Contains information about a poll (includes correct_option_ids, allows_revoting, description, description_entities). | Bot API 4.2 (updated 10.1) |
| [`PollOptionAdded`](https://core.telegram.org/bots/api#polloptionadded) | Service message: an option was added to a poll. | Bot API 9.6 |
| [`PollOptionDeleted`](https://core.telegram.org/bots/api#polloptiondeleted) | Service message: an option was deleted from a poll. | Bot API 9.6 |
| [`ChecklistTask`](https://core.telegram.org/bots/api#checklisttask) | Describes a task in a checklist (id, text, text_entities, completed_by_user, completed_by_chat, completion_date). | Bot API 9.1 (updated 9.2) |
| [`Checklist`](https://core.telegram.org/bots/api#checklist) | Describes a checklist (title, title_entities, tasks, others_can_add_tasks, others_can_mark_tasks_as_done). | Bot API 9.1 |
| [`InputChecklistTask`](https://core.telegram.org/bots/api#inputchecklisttask) | Describes a task to add to a checklist (id, text, parse_mode, text_entities). | Bot API 9.1 |
| [`InputChecklist`](https://core.telegram.org/bots/api#inputchecklist) | Describes a checklist to create (title, parse_mode, title_entities, tasks, others_can_add_tasks, others_can_mark_tasks_as_done). | Bot API 9.1 |
| [`ChecklistTasksDone`](https://core.telegram.org/bots/api#checklisttasksdone) | Service message: tasks in a checklist were marked as done or not done. | Bot API 9.1 |
| [`ChecklistTasksAdded`](https://core.telegram.org/bots/api#checklisttasksadded) | Service message: tasks were added to a checklist. | Bot API 9.1 |
| [`Location`](https://core.telegram.org/bots/api#location) | Represents a point on the map. | Bot API 1.0 |
| [`Venue`](https://core.telegram.org/bots/api#venue) | Represents a venue. | Bot API 2.0 |
| [`WebAppData`](https://core.telegram.org/bots/api#webappdata) | Describes data sent from a Web App to the bot via Telegram.WebApp.sendData. | Bot API 6.0 |
| [`ProximityAlertTriggered`](https://core.telegram.org/bots/api#proximityalerttriggered) | Service message: a user in the chat triggered another user's proximity alert. | Bot API 5.0 |
| [`UserProfilePhotos`](https://core.telegram.org/bots/api#userprofilephotos) | Represents a user's profile pictures. | Bot API 1.0 |
| [`UserProfileAudios`](https://core.telegram.org/bots/api#userprofileaudios) | Represents a user's profile audio tracks. | Bot API 9.4 |
| [`File`](https://core.telegram.org/bots/api#file) | Represents a file ready to be downloaded (file_id, file_unique_id, file_size, file_path). | Bot API 1.0 |
| [`InputFile`](https://core.telegram.org/bots/api#inputfile) | Represents the contents of a file to be uploaded via multipart/form-data or URL/file_id. | Bot API 1.0 |
| [`InputProfilePhoto`](https://core.telegram.org/bots/api#inputprofilephoto) | Union of InputProfilePhotoStatic | InputProfilePhotoAnimated. | Bot API 9.0 |

## InputMedia & InputPaidMedia (11)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`InputProfilePhotoStatic`](https://core.telegram.org/bots/api#inputprofilephotostatic) | A static profile photo in the .JPG format. | Bot API 9.0 |
| [`InputProfilePhotoAnimated`](https://core.telegram.org/bots/api#inputprofilephotoanimated) | An animated profile photo in the MPEG4 format. | Bot API 9.0 |
| [`InputMedia`](https://core.telegram.org/bots/api#inputmedia) | Union of InputMediaAnimation | InputMediaDocument | InputMediaAudio | InputMediaPhoto | InputMediaVideo. | Bot API 3.5 |
| [`InputMediaPhoto`](https://core.telegram.org/bots/api#inputmediaphoto) | Represents a photo to be sent. | Bot API 3.5 |
| [`InputMediaVideo`](https://core.telegram.org/bots/api#inputmediavideo) | Represents a video to be sent (supports cover, start_timestamp). | Bot API 3.5 (updated 8.3) |
| [`InputMediaAnimation`](https://core.telegram.org/bots/api#inputmediaanimation) | Represents an animation file to be sent. | Bot API 4.0 |
| [`InputMediaAudio`](https://core.telegram.org/bots/api#inputmediaaudio) | Represents an audio file to be sent. | Bot API 4.0 |
| [`InputMediaDocument`](https://core.telegram.org/bots/api#inputmediadocument) | Represents a general file to be sent. | Bot API 4.0 |
| [`InputPaidMedia`](https://core.telegram.org/bots/api#inputpaidmedia) | Union of InputPaidMediaPhoto | InputPaidMediaVideo. | Bot API 7.6 |
| [`InputPaidMediaPhoto`](https://core.telegram.org/bots/api#inputpaidmediaphoto) | The paid media to send is a photo. | Bot API 7.6 |
| [`InputPaidMediaVideo`](https://core.telegram.org/bots/api#inputpaidmediavideo) | The paid media to send is a video. | Bot API 7.6 |

## In-Chat HTML Widgets & TON Wallet (Bot API 10.4) (15)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`Widget`](https://core.telegram.org/bots/api#widget) | Represents an interactive per-user HTML widget in a message (url, aspect_ratio, data). | Bot API 10.4 |
| [`SharedWidget`](https://core.telegram.org/bots/api#sharedwidget) | Represents a shared interactive HTML widget in a message (url, aspect_ratio, data). | Bot API 10.4 |
| [`WidgetQuery`](https://core.telegram.org/bots/api#widgetquery) | Represents an incoming query from a per-user Widget (id, from, message, inline_message_id, chat_instance, data, type). | Bot API 10.4 |
| [`SharedWidgetQuery`](https://core.telegram.org/bots/api#sharedwidgetquery) | Represents an incoming query from a SharedWidget (id, from, message, inline_message_id, chat_instance, data, type). | Bot API 10.4 |
| [`WidgetQueryType`](https://core.telegram.org/bots/api#widgetquerytype) | Union of WidgetQueryTypeRegular | WidgetQueryTypeShareScore | WidgetQueryTypeStartTransaction. | Bot API 10.4 |
| [`WidgetQueryTypeRegular`](https://core.telegram.org/bots/api#widgetquerytyperegular) | Regular widget query triggered by window.TelegramWidget.sendQuery. | Bot API 10.4 |
| [`WidgetQueryTypeShareScore`](https://core.telegram.org/bots/api#widgetquerytypesharescore) | Widget query requesting to share a game/widget score. | Bot API 10.4 |
| [`WidgetQueryTypeStartTransaction`](https://core.telegram.org/bots/api#widgetquerytypestarttransaction) | Widget query requesting to initiate a TON wallet or payment transaction. | Bot API 10.4 |
| [`WidgetQueryWallet`](https://core.telegram.org/bots/api#widgetquerywallet) | Contains TON wallet details attached to a widget query. | Bot API 10.4 |
| [`TonWalletCard`](https://core.telegram.org/bots/api#tonwalletcard) | Represents a user's TON wallet card metadata. | Bot API 10.4 |
| [`TonWalletCardSticker`](https://core.telegram.org/bots/api#tonwalletcardsticker) | Represents a sticker placed on a TON wallet card (sticker, position: AreaPosition). | Bot API 10.4 |
| [`TonNft`](https://core.telegram.org/bots/api#tonnft) | Represents a TON NFT collectible item. | Bot API 10.4 |
| [`TonNftAttribute`](https://core.telegram.org/bots/api#tonnftattribute) | Represents an attribute/trait of a TON NFT. | Bot API 10.4 |
| [`TonWalletTransfer`](https://core.telegram.org/bots/api#tonwallettransfer) | Service message / payload describing a TON wallet transfer. | Bot API 10.4 |
| [`AreaPosition`](https://core.telegram.org/bots/api#areaposition) | Describes the 2D position, size, and rotation of an element on a card or story. | Bot API 10.4 |

## Keyboards, Buttons & WebAppInfo (15)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`WebAppInfo`](https://core.telegram.org/bots/api#webappinfo) | Describes a Web App (url). | Bot API 6.0 |
| [`ReplyKeyboardMarkup`](https://core.telegram.org/bots/api#replykeyboardmarkup) | Represents a custom keyboard with reply options (keyboard, is_persistent, resize_keyboard, one_time_keyboard, input_field_placeholder, selective). | Bot API 1.0 (updated 6.4) |
| [`KeyboardButton`](https://core.telegram.org/bots/api#keyboardbutton) | Represents one button of a reply keyboard (includes icon_custom_emoji_id, style: 'danger'|'success'|'primary', request_users, request_chat, request_managed_bot, request_contact, request_location, request_poll, web_app). | Bot API 1.0 (updated 9.6) |
| [`KeyboardButtonRequestUsers`](https://core.telegram.org/bots/api#keyboardbuttonrequestusers) | Defines the criteria used to request suitable users. | Bot API 7.0 (updated 7.2) |
| [`KeyboardButtonRequestChat`](https://core.telegram.org/bots/api#keyboardbuttonrequestchat) | Defines the criteria used to request a suitable chat. | Bot API 6.5 (updated 7.2) |
| [`KeyboardButtonRequestManagedBot`](https://core.telegram.org/bots/api#keyboardbuttonrequestmanagedbot) | Defines the criteria used to create a managed bot on behalf of the user. | Bot API 9.6 |
| [`KeyboardButtonPollType`](https://core.telegram.org/bots/api#keyboardbuttonpolltype) | Represents type of a poll which is allowed to be created. | Bot API 4.7 |
| [`ReplyKeyboardRemove`](https://core.telegram.org/bots/api#replykeyboardremove) | Requests clients to remove the custom keyboard. | Bot API 2.3 |
| [`InlineKeyboardMarkup`](https://core.telegram.org/bots/api#inlinekeyboardmarkup) | Represents an inline keyboard that appears right next to the message it belongs to. | Bot API 2.0 |
| [`InlineKeyboardButton`](https://core.telegram.org/bots/api#inlinekeyboardbutton) | Represents one button of an inline keyboard (includes icon_custom_emoji_id, style: 'danger'|'success'|'primary', url, callback_data, web_app, login_url, switch_inline_query, switch_inline_query_current_chat, switch_inline_query_chosen_chat, copy_text, callback_game, pay). | Bot API 2.0 (updated 9.4) |
| [`LoginUrl`](https://core.telegram.org/bots/api#loginurl) | Represents a parameter of the inline keyboard button used to automatically authorize a user. | Bot API 4.3 |
| [`SwitchInlineQueryChosenChat`](https://core.telegram.org/bots/api#switchinlinequerychosenchat) | Represents an inline button that switches the current user to inline mode in a chosen chat. | Bot API 6.7 |
| [`CopyTextButton`](https://core.telegram.org/bots/api#copytextbutton) | Represents an inline keyboard button that copies specified text to the clipboard (text: 1-256 chars). | Bot API 7.11 |
| [`CallbackQuery`](https://core.telegram.org/bots/api#callbackquery) | Represents an incoming callback query from a callback button in an inline keyboard. | Bot API 2.0 |
| [`ForceReply`](https://core.telegram.org/bots/api#forcereply) | Upon receiving a message with this object, Telegram clients will display a reply interface to the user. | Bot API 1.0 |

## Chat Members, Permissions, Invites & Themes (28)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`ChatPhoto`](https://core.telegram.org/bots/api#chatphoto) | Represents a chat photo. | Bot API 2.1 |
| [`ChatInviteLink`](https://core.telegram.org/bots/api#chatinvitelink) | Represents an invite link for a chat. | Bot API 5.1 (updated 7.9) |
| [`ChatAdministratorRights`](https://core.telegram.org/bots/api#chatadministratorrights) | Represents the rights of an administrator in a chat (includes can_manage_direct_messages, can_manage_tags). | Bot API 6.0 (updated 9.5) |
| [`ChatMemberUpdated`](https://core.telegram.org/bots/api#chatmemberupdated) | Represents changes in the status of a chat member. | Bot API 5.1 |
| [`ChatMember`](https://core.telegram.org/bots/api#chatmember) | Union of ChatMemberOwner | ChatMemberAdministrator | ChatMemberMember | ChatMemberRestricted | ChatMemberLeft | ChatMemberBanned. | Bot API 2.1 |
| [`ChatMemberOwner`](https://core.telegram.org/bots/api#chatmemberowner) | Represents a chat member that owns the chat and has all administrator privileges. | Bot API 5.3 |
| [`ChatMemberAdministrator`](https://core.telegram.org/bots/api#chatmemberadministrator) | Represents a chat member that has some additional privileges. | Bot API 5.3 (updated 9.5) |
| [`ChatMemberMember`](https://core.telegram.org/bots/api#chatmembermember) | Represents a chat member that has no additional privileges or restrictions (includes until_date, tag). | Bot API 5.3 (updated 9.5) |
| [`ChatMemberRestricted`](https://core.telegram.org/bots/api#chatmemberrestricted) | Represents a chat member that is under certain restrictions in the chat (includes tag). | Bot API 5.3 (updated 9.5) |
| [`ChatMemberLeft`](https://core.telegram.org/bots/api#chatmemberleft) | Represents a chat member that isn't currently a member of the chat, but may join it themselves. | Bot API 5.3 |
| [`ChatMemberBanned`](https://core.telegram.org/bots/api#chatmemberbanned) | Represents a chat member that was banned in the chat and can't return to the chat. | Bot API 5.3 |
| [`ChatJoinRequest`](https://core.telegram.org/bots/api#chatjoinrequest) | Represents a join request sent to a chat. | Bot API 5.4 |
| [`ChatPermissions`](https://core.telegram.org/bots/api#chatpermissions) | Describes actions that a non-administrator user is allowed to take in a chat (includes can_edit_tag). | Bot API 4.4 (updated 9.5) |
| [`Birthdate`](https://core.telegram.org/bots/api#birthdate) | Describes the birthdate of a user. | Bot API 7.2 |
| [`ChatLocation`](https://core.telegram.org/bots/api#chatlocation) | Represents a location to which a chat is connected. | Bot API 5.0 |
| [`UserRating`](https://core.telegram.org/bots/api#userrating) | Describes the rating/level of a user based on their Telegram activity. | Bot API 9.3 |
| [`ChatShareTheme`](https://core.telegram.org/bots/api#chatsharetheme) | Union of ChatShareThemePredefined | ChatShareThemeCustom. | Bot API 10.4 |
| [`ChatShareThemePredefined`](https://core.telegram.org/bots/api#chatsharethemepredefined) | Represents a predefined chat share theme by name. | Bot API 10.4 |
| [`ChatShareThemeCustom`](https://core.telegram.org/bots/api#chatsharethemecustom) | Represents a custom chat share theme with custom colors, pattern, and backdrop. | Bot API 10.4 |
| [`ChatShareThemeBackdrop`](https://core.telegram.org/bots/api#chatsharethemebackdrop) | Describes a backdrop style available for custom chat share themes. | Bot API 10.4 |
| [`ChatShareThemeColors`](https://core.telegram.org/bots/api#chatsharethemecolors) | Describes the color palette of a custom chat share theme. | Bot API 10.4 |
| [`ChatShareThemePattern`](https://core.telegram.org/bots/api#chatsharethemepattern) | Describes the background pattern of a custom chat share theme. | Bot API 10.4 |
| [`EmojiType`](https://core.telegram.org/bots/api#emojitype) | Union of EmojiTypeRegular | EmojiTypeCustom. | Bot API 10.4 |
| [`EmojiTypeRegular`](https://core.telegram.org/bots/api#emojityperegular) | Represents a standard Unicode emoji. | Bot API 10.4 |
| [`EmojiTypeCustom`](https://core.telegram.org/bots/api#emojitypecustom) | Represents a Telegram custom emoji by custom_emoji_id. | Bot API 10.4 |
| [`ChatThemeChanged`](https://core.telegram.org/bots/api#chatthemechanged) | Service message: the chat theme was changed. | Bot API 10.4 |
| [`ChatOwnerLeft`](https://core.telegram.org/bots/api#chatownerleft) | Service message: the chat owner left the chat. | Bot API 9.4 |
| [`ChatOwnerChanged`](https://core.telegram.org/bots/api#chatownerchanged) | Service message: chat ownership was transferred to another member. | Bot API 9.4 |

## Business, Gifts, Stories, Suggested Posts & Boosts (56)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`BusinessIntro`](https://core.telegram.org/bots/api#businessintro) | Contains information about the start page settings of a Telegram Business account. | Bot API 7.2 |
| [`BusinessLocation`](https://core.telegram.org/bots/api#businesslocation) | Contains information about the location of a Telegram Business account. | Bot API 7.2 |
| [`BusinessOpeningHoursInterval`](https://core.telegram.org/bots/api#businessopeninghoursinterval) | Describes an interval of time during which a business is open. | Bot API 7.2 |
| [`BusinessOpeningHours`](https://core.telegram.org/bots/api#businessopeninghours) | Describes the opening hours of a business. | Bot API 7.2 |
| [`BusinessConnection`](https://core.telegram.org/bots/api#businessconnection) | Describes the connection of the bot with a business account (rights: BusinessBotRights). | Bot API 7.2 (updated 9.0) |
| [`BusinessMessagesDeleted`](https://core.telegram.org/bots/api#businessmessagesdeleted) | This object is received when messages are deleted from a connected business account. | Bot API 7.2 |
| [`BusinessBotRights`](https://core.telegram.org/bots/api#businessbotrights) | Represents the rights of a business bot (can_reply, can_read_messages, can_delete_sent_messages, can_delete_all_messages, can_edit_name, can_edit_bio, can_edit_profile_photo, can_edit_username, can_change_gift_settings, can_view_gifts_and_stars, can_convert_gifts_to_stars, can_transfer_and_upgrade_gifts, can_transfer_stars, can_manage_stories). | Bot API 9.0 |
| [`StoryAreaPosition`](https://core.telegram.org/bots/api#storyareaposition) | Describes the position of a clickable area within a story. | Bot API 9.0 |
| [`LocationAddress`](https://core.telegram.org/bots/api#locationaddress) | Describes the physical address of a location. | Bot API 9.0 |
| [`StoryAreaType`](https://core.telegram.org/bots/api#storyareatype) | Union of StoryAreaTypeLocation | StoryAreaTypeSuggestedReaction | StoryAreaTypeLink | StoryAreaTypeWeather | StoryAreaTypeUniqueGift. | Bot API 9.0 |
| [`StoryAreaTypeLocation`](https://core.telegram.org/bots/api#storyareatypelocation) | Describes a story area pointing to a location. | Bot API 9.0 |
| [`StoryAreaTypeSuggestedReaction`](https://core.telegram.org/bots/api#storyareatypesuggestedreaction) | Describes a story area pointing to a suggested reaction. | Bot API 9.0 |
| [`StoryAreaTypeLink`](https://core.telegram.org/bots/api#storyareatypelink) | Describes a story area pointing to an HTTP or tg:// link. | Bot API 9.0 |
| [`StoryAreaTypeWeather`](https://core.telegram.org/bots/api#storyareatypeweather) | Describes a story area containing weather information. | Bot API 9.0 |
| [`StoryAreaTypeUniqueGift`](https://core.telegram.org/bots/api#storyareatypeuniquegift) | Describes a story area pointing to a unique gift. | Bot API 9.0 |
| [`StoryArea`](https://core.telegram.org/bots/api#storyarea) | Describes a clickable area on a story media. | Bot API 9.0 |
| [`InputStoryContent`](https://core.telegram.org/bots/api#inputstorycontent) | Union of InputStoryContentPhoto | InputStoryContentVideo. | Bot API 9.0 |
| [`InputStoryContentPhoto`](https://core.telegram.org/bots/api#inputstorycontentphoto) | Describes a photo to post as a story. | Bot API 9.0 |
| [`InputStoryContentVideo`](https://core.telegram.org/bots/api#inputstorycontentvideo) | Describes a video to post as a story. | Bot API 9.0 |
| [`GiftBackground`](https://core.telegram.org/bots/api#giftbackground) | Describes the background of a gift. | Bot API 9.4 |
| [`Gift`](https://core.telegram.org/bots/api#gift) | Represents a gift that can be sent by the bot. | Bot API 8.0 (updated 9.4) |
| [`Gifts`](https://core.telegram.org/bots/api#gifts) | Represent a list of gifts. | Bot API 8.0 |
| [`UniqueGiftModel`](https://core.telegram.org/bots/api#uniquegiftmodel) | Describes the model of a unique gift (includes rarity). | Bot API 9.0 (updated 9.4) |
| [`UniqueGiftSymbol`](https://core.telegram.org/bots/api#uniquegiftsymbol) | Describes the symbol shown on the pattern of a unique gift. | Bot API 9.0 |
| [`UniqueGiftBackdropColors`](https://core.telegram.org/bots/api#uniquegiftbackdropcolors) | Describes the colors of the backdrop of a unique gift. | Bot API 9.0 |
| [`UniqueGiftBackdrop`](https://core.telegram.org/bots/api#uniquegiftbackdrop) | Describes the backdrop of a unique gift. | Bot API 9.0 |
| [`UniqueGiftColors`](https://core.telegram.org/bots/api#uniquegiftcolors) | Contains information about the color scheme for a user's name, message replies, and link previews based on a unique gift. | Bot API 9.3 |
| [`UniqueGift`](https://core.telegram.org/bots/api#uniquegift) | Describes a unique gift that was upgraded from a regular gift (includes gift_id, is_from_blockchain, is_premium, is_burned, colors, publisher_chat). | Bot API 9.0 (updated 9.5) |
| [`GiftInfo`](https://core.telegram.org/bots/api#giftinfo) | Describes a service message about a regular gift that was sent or received. | Bot API 9.0 (updated 9.3) |
| [`UniqueGiftInfo`](https://core.telegram.org/bots/api#uniquegiftinfo) | Describes a service message or lookup response about a unique gift. | Bot API 9.0 (updated 10.4) |
| [`OwnedGift`](https://core.telegram.org/bots/api#ownedgift) | Union of OwnedGiftRegular | OwnedGiftUnique. | Bot API 9.0 |
| [`OwnedGiftRegular`](https://core.telegram.org/bots/api#ownedgiftregular) | Describes a regular gift owned by a user or a chat. | Bot API 9.0 (updated 9.3) |
| [`OwnedGiftUnique`](https://core.telegram.org/bots/api#ownedgiftunique) | Describes a unique gift owned by a user or a chat. | Bot API 9.0 (updated 9.3) |
| [`OwnedGifts`](https://core.telegram.org/bots/api#ownedgifts) | Contains the list of gifts received and owned by a user or a chat. | Bot API 9.0 |
| [`AcceptedGiftTypes`](https://core.telegram.org/bots/api#acceptedgifttypes) | Describes the types of gifts that can be gifted to a user or a chat (unlimited_gifts, limited_gifts, unique_gifts, premium_subscription, gifts_from_channels). | Bot API 9.0 (updated 9.3) |
| [`StarAmount`](https://core.telegram.org/bots/api#staramount) | Describes an amount of Telegram Stars (amount, nanostar_amount). | Bot API 9.0 |
| [`SuggestedPostPrice`](https://core.telegram.org/bots/api#suggestedpostprice) | Describes the price of a suggested post (currency: 'XTR'|'TON', amount). | Bot API 9.2 |
| [`SuggestedPostInfo`](https://core.telegram.org/bots/api#suggestedpostinfo) | Contains information about a suggested post. | Bot API 9.2 |
| [`SuggestedPostParameters`](https://core.telegram.org/bots/api#suggestedpostparameters) | Contains parameters of a post that is being suggested by the bot. | Bot API 9.2 |
| [`SuggestedPostApproved`](https://core.telegram.org/bots/api#suggestedpostapproved) | Service message: a suggested post was approved. | Bot API 9.2 |
| [`SuggestedPostApprovalFailed`](https://core.telegram.org/bots/api#suggestedpostapprovalfailed) | Service message: approval of a suggested post has failed. | Bot API 9.2 |
| [`SuggestedPostDeclined`](https://core.telegram.org/bots/api#suggestedpostdeclined) | Service message: a suggested post was declined. | Bot API 9.2 |
| [`SuggestedPostPaid`](https://core.telegram.org/bots/api#suggestedpostpaid) | Service message: payment for a suggested post was received. | Bot API 9.2 |
| [`SuggestedPostRefunded`](https://core.telegram.org/bots/api#suggestedpostrefunded) | Service message: payment for a suggested post was refunded. | Bot API 9.2 |
| [`GiveawayCreated`](https://core.telegram.org/bots/api#giveawaycreated) | Service message: a scheduled giveaway was created. | Bot API 7.0 (updated 7.9) |
| [`Giveaway`](https://core.telegram.org/bots/api#giveaway) | Represents a message about a scheduled giveaway. | Bot API 7.0 (updated 7.9) |
| [`GiveawayWinners`](https://core.telegram.org/bots/api#giveawaywinners) | Represents a message about the completion of a giveaway with public winners. | Bot API 7.0 (updated 7.9) |
| [`GiveawayCompleted`](https://core.telegram.org/bots/api#giveawaycompleted) | Service message: a giveaway without public winners was completed. | Bot API 7.0 (updated 7.9) |
| [`ChatBoostSource`](https://core.telegram.org/bots/api#chatboostsource) | Union of ChatBoostSourcePremium | ChatBoostSourceGiftCode | ChatBoostSourceGiveaway. | Bot API 7.0 |
| [`ChatBoostSourcePremium`](https://core.telegram.org/bots/api#chatboostsourcepremium) | The boost was obtained by subscribing to Telegram Premium. | Bot API 7.0 |
| [`ChatBoostSourceGiftCode`](https://core.telegram.org/bots/api#chatboostsourcegiftcode) | The boost was obtained by the creation of Telegram Premium gift codes. | Bot API 7.0 |
| [`ChatBoostSourceGiveaway`](https://core.telegram.org/bots/api#chatboostsourcegiveaway) | The boost was obtained by the creation of a Telegram Premium or Telegram Star giveaway. | Bot API 7.0 (updated 7.9) |
| [`ChatBoost`](https://core.telegram.org/bots/api#chatboost) | Contains information about a chat boost. | Bot API 7.0 |
| [`ChatBoostUpdated`](https://core.telegram.org/bots/api#chatboostupdated) | Represents a boost added to a chat or changed. | Bot API 7.0 |
| [`ChatBoostRemoved`](https://core.telegram.org/bots/api#chatboostremoved) | Represents a boost removed from a chat. | Bot API 7.0 |
| [`UserChatBoosts`](https://core.telegram.org/bots/api#userchatboosts) | Represents a list of boosts added to a chat by a user. | Bot API 7.0 |

## Forum Topics, Reactions, Commands, Menu & Background (45)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`ForumTopic`](https://core.telegram.org/bots/api#forumtopic) | Represents a forum topic (message_thread_id, name, icon_color, icon_custom_emoji_id, is_name_implicit). | Bot API 6.3 (updated 9.3) |
| [`ForumTopicCreated`](https://core.telegram.org/bots/api#forumtopiccreated) | Service message: a new forum topic was created in the chat. | Bot API 6.3 (updated 9.3) |
| [`ForumTopicClosed`](https://core.telegram.org/bots/api#forumtopicclosed) | Service message: a forum topic was closed in the chat. | Bot API 6.3 |
| [`ForumTopicEdited`](https://core.telegram.org/bots/api#forumtopicedited) | Service message: a forum topic was edited. | Bot API 6.4 |
| [`ForumTopicReopened`](https://core.telegram.org/bots/api#forumtopicreopened) | Service message: a forum topic was reopened. | Bot API 6.3 |
| [`GeneralForumTopicHidden`](https://core.telegram.org/bots/api#generalforumtopichidden) | Service message: the 'General' forum topic was hidden. | Bot API 6.4 |
| [`GeneralForumTopicUnhidden`](https://core.telegram.org/bots/api#generalforumtopicunhidden) | Service message: the 'General' forum topic was unhidden. | Bot API 6.4 |
| [`SharedUser`](https://core.telegram.org/bots/api#shareduser) | Contains information about a user that was shared with the bot using a KeyboardButtonRequestUsers button. | Bot API 7.2 |
| [`VideoChatScheduled`](https://core.telegram.org/bots/api#videochatscheduled) | Service message: a video chat was scheduled in the chat. | Bot API 5.2 (renamed 6.0) |
| [`VideoChatStarted`](https://core.telegram.org/bots/api#videochatstarted) | Service message: a video chat was started in the chat. | Bot API 5.1 (renamed 6.0) |
| [`VideoChatEnded`](https://core.telegram.org/bots/api#videochatended) | Service message: a video chat was ended in the chat. | Bot API 5.1 (renamed 6.0) |
| [`VideoChatParticipantsInvited`](https://core.telegram.org/bots/api#videochatparticipantsinvited) | Service message: new participants were invited to a video chat. | Bot API 5.1 (renamed 6.0) |
| [`ReactionType`](https://core.telegram.org/bots/api#reactiontype) | Union of ReactionTypeEmoji | ReactionTypeCustomEmoji | ReactionTypePaid. | Bot API 7.0 (updated 7.9) |
| [`ReactionTypeEmoji`](https://core.telegram.org/bots/api#reactiontypeemoji) | The reaction is based on a standard emoji. | Bot API 7.0 |
| [`ReactionTypeCustomEmoji`](https://core.telegram.org/bots/api#reactiontypecustomemoji) | The reaction is based on a custom emoji. | Bot API 7.0 |
| [`ReactionTypePaid`](https://core.telegram.org/bots/api#reactiontypepaid) | The reaction is paid with Telegram Stars. | Bot API 7.9 |
| [`ReactionCount`](https://core.telegram.org/bots/api#reactioncount) | Represents a reaction added to a message along with the number of times it was added. | Bot API 7.0 |
| [`MessageReactionUpdated`](https://core.telegram.org/bots/api#messagereactionupdated) | Represents a change of a reaction on a message performed by a user. | Bot API 7.0 |
| [`MessageReactionCountUpdated`](https://core.telegram.org/bots/api#messagereactioncountupdated) | Represents reaction changes on a message with anonymous reactions. | Bot API 7.0 |
| [`BotCommand`](https://core.telegram.org/bots/api#botcommand) | Represents a bot command (command: 1-32 chars, description: 1-256 chars). | Bot API 4.7 |
| [`BotCommandScope`](https://core.telegram.org/bots/api#botcommandscope) | Union of 7 BotCommandScope* types. | Bot API 5.3 |
| [`BotCommandScopeDefault`](https://core.telegram.org/bots/api#botcommandscopedefault) | Represents the default scope of bot commands. | Bot API 5.3 |
| [`BotCommandScopeAllPrivateChats`](https://core.telegram.org/bots/api#botcommandscopeallprivatechats) | Represents the scope of bot commands covering all private chats. | Bot API 5.3 |
| [`BotCommandScopeAllGroupChats`](https://core.telegram.org/bots/api#botcommandscopeallgroupchats) | Represents the scope of bot commands covering all group and supergroup chats. | Bot API 5.3 |
| [`BotCommandScopeAllChatAdministrators`](https://core.telegram.org/bots/api#botcommandscopeallchatadministrators) | Represents the scope of bot commands covering all group and supergroup chat administrators. | Bot API 5.3 |
| [`BotCommandScopeChat`](https://core.telegram.org/bots/api#botcommandscopechat) | Represents the scope of bot commands covering a specific chat. | Bot API 5.3 |
| [`BotCommandScopeChatAdministrators`](https://core.telegram.org/bots/api#botcommandscopechatadministrators) | Represents the scope of bot commands covering all administrators of a specific group or supergroup chat. | Bot API 5.3 |
| [`BotCommandScopeChatMember`](https://core.telegram.org/bots/api#botcommandscopechatmember) | Represents the scope of bot commands covering a specific member of a group or supergroup chat. | Bot API 5.3 |
| [`BotName`](https://core.telegram.org/bots/api#botname) | Represents the bot's name. | Bot API 6.6 |
| [`BotDescription`](https://core.telegram.org/bots/api#botdescription) | Represents the bot's description. | Bot API 6.6 |
| [`BotShortDescription`](https://core.telegram.org/bots/api#botshortdescription) | Represents the bot's short description. | Bot API 6.6 |
| [`MenuButton`](https://core.telegram.org/bots/api#menubutton) | Union of MenuButtonCommands | MenuButtonWebApp | MenuButtonDefault. | Bot API 6.0 |
| [`MenuButtonCommands`](https://core.telegram.org/bots/api#menubuttoncommands) | Represents a menu button, which opens the bot's list of commands. | Bot API 6.0 |
| [`MenuButtonWebApp`](https://core.telegram.org/bots/api#menubuttonwebapp) | Represents a menu button, which launches a Web App. | Bot API 6.0 |
| [`MenuButtonDefault`](https://core.telegram.org/bots/api#menubuttondefault) | Describes that no specific value for the menu button was set. | Bot API 6.0 |
| [`BackgroundFill`](https://core.telegram.org/bots/api#backgroundfill) | Union of BackgroundFillSolid | BackgroundFillGradient | BackgroundFillFreeformGradient. | Bot API 7.3 |
| [`BackgroundFillSolid`](https://core.telegram.org/bots/api#backgroundfillsolid) | The background is filled using the selected color. | Bot API 7.3 |
| [`BackgroundFillGradient`](https://core.telegram.org/bots/api#backgroundfillgradient) | The background is a gradient fill. | Bot API 7.3 |
| [`BackgroundFillFreeformGradient`](https://core.telegram.org/bots/api#backgroundfillfreeformgradient) | The background is a freeform gradient that rotates after every message in the chat. | Bot API 7.3 |
| [`BackgroundType`](https://core.telegram.org/bots/api#backgroundtype) | Union of BackgroundTypeFill | BackgroundTypeWallpaper | BackgroundTypePattern | BackgroundTypeChatTheme. | Bot API 7.3 |
| [`BackgroundTypeFill`](https://core.telegram.org/bots/api#backgroundtypefill) | The background is automatically filled based on the selected colors. | Bot API 7.3 |
| [`BackgroundTypeWallpaper`](https://core.telegram.org/bots/api#backgroundtypewallpaper) | The background is a wallpaper in the JPEG format. | Bot API 7.3 |
| [`BackgroundTypePattern`](https://core.telegram.org/bots/api#backgroundtypepattern) | The background is a .PNG or .TGV pattern to be combined with the background fill. | Bot API 7.3 |
| [`BackgroundTypeChatTheme`](https://core.telegram.org/bots/api#backgroundtypechattheme) | The background is taken directly from a built-in chat theme. | Bot API 7.3 |
| [`ChatBackground`](https://core.telegram.org/bots/api#chatbackground) | This object represents a chat background. | Bot API 7.3 |

## Stickers (4)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`Sticker`](https://core.telegram.org/bots/api#sticker) | Represents a sticker. | Bot API 1.0 (updated 6.6) |
| [`StickerSet`](https://core.telegram.org/bots/api#stickerset) | Represents a sticker set. | Bot API 3.2 (updated 7.2) |
| [`MaskPosition`](https://core.telegram.org/bots/api#maskposition) | Describes the position on faces where a mask should be placed by default. | Bot API 3.2 |
| [`InputSticker`](https://core.telegram.org/bots/api#inputsticker) | Describes a sticker to be added to a sticker set. | Bot API 6.6 (updated 7.2) |

## Rich Messages (Bot API 10.2–10.4) (82)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`RichMessage`](https://core.telegram.org/bots/api#richmessage) | Represents a structured multi-block rich message (title, subtitle, blocks: Array of RichBlock, buttons: Array of RichMessageButton). | Bot API 10.2 |
| [`InputRichMessage`](https://core.telegram.org/bots/api#inputrichmessage) | Describes a structured rich message to be sent via sendRichMessage / sendRichMessageDraft. | Bot API 10.2 |
| [`InputRichMessageMedia`](https://core.telegram.org/bots/api#inputrichmessagemedia) | Describes media attached inside an InputRichMessage block. | Bot API 10.2 |
| [`RichMessageButton`](https://core.telegram.org/bots/api#richmessagebutton) | Represents an interactive button attached to a RichMessage. | Bot API 10.2 |
| [`RichText`](https://core.telegram.org/bots/api#richtext) | Union of 13 RichText* inline text formatting nodes (including RichTextTonAddress in 10.4). | Bot API 10.2 (updated 10.4) |
| [`RichTextPlain`](https://core.telegram.org/bots/api#richtextplain) | Plain unformatted text node inside RichText. | Bot API 10.2 |
| [`RichTextBold`](https://core.telegram.org/bots/api#richtextbold) | Bold RichText node. | Bot API 10.2 |
| [`RichTextItalic`](https://core.telegram.org/bots/api#richtextitalic) | Italic RichText node. | Bot API 10.2 |
| [`RichTextUnderline`](https://core.telegram.org/bots/api#richtextunderline) | Underlined RichText node. | Bot API 10.2 |
| [`RichTextStrikethrough`](https://core.telegram.org/bots/api#richtextstrikethrough) | Strikethrough RichText node. | Bot API 10.2 |
| [`RichTextSpoiler`](https://core.telegram.org/bots/api#richtextspoiler) | Spoiler RichText node. | Bot API 10.2 |
| [`RichTextMarked`](https://core.telegram.org/bots/api#richtextmarked) | Highlighted/marked RichText node. | Bot API 10.2 |
| [`RichTextCode`](https://core.telegram.org/bots/api#richtextcode) | Monospace inline code RichText node. | Bot API 10.2 |
| [`RichTextSubscript`](https://core.telegram.org/bots/api#richtextsubscript) | Subscript RichText node. | Bot API 10.2 |
| [`RichTextSuperscript`](https://core.telegram.org/bots/api#richtextsuperscript) | Superscript RichText node. | Bot API 10.2 |
| [`RichTextUrl`](https://core.telegram.org/bots/api#richtexturl) | Hyperlink RichText node. | Bot API 10.2 |
| [`RichTextEmailAddress`](https://core.telegram.org/bots/api#richtextemailaddress) | Email link RichText node. | Bot API 10.2 |
| [`RichTextPhoneNumber`](https://core.telegram.org/bots/api#richtextphonenumber) | Phone number RichText node. | Bot API 10.2 |
| [`RichTextTonAddress`](https://core.telegram.org/bots/api#richtexttonaddress) | TON cryptocurrency address RichText node. | Bot API 10.4 |
| [`RichTextAnchorLink`](https://core.telegram.org/bots/api#richtextanchorlink) | Internal anchor link RichText node. | Bot API 10.2 |
| [`RichTextIcon`](https://core.telegram.org/bots/api#richtexticon) | Inline icon/custom emoji RichText node. | Bot API 10.2 |
| [`RichTextDateTime`](https://core.telegram.org/bots/api#richtextdatetime) | Localized date/time RichText node. | Bot API 10.2 |
| [`RichTextReference`](https://core.telegram.org/bots/api#richtextreference) | Footnote/reference RichText node. | Bot API 10.2 |
| [`RichTextConcat`](https://core.telegram.org/bots/api#richtextconcat) | Concatenation of multiple RichText nodes. | Bot API 10.2 |
| [`RichBlockCaption`](https://core.telegram.org/bots/api#richblockcaption) | Caption and credit metadata for a RichBlock media item. | Bot API 10.2 |
| [`RichBlockTableCell`](https://core.telegram.org/bots/api#richblocktablecell) | Represents a cell inside a RichBlockTable. | Bot API 10.2 |
| [`RichBlockListItem`](https://core.telegram.org/bots/api#richblocklistitem) | Represents an item inside a RichBlockList. | Bot API 10.2 |
| [`RichBlock`](https://core.telegram.org/bots/api#richblock) | Union of 25 RichBlock* structural block types. | Bot API 10.2 |
| [`RichBlockTitle`](https://core.telegram.org/bots/api#richblocktitle) | Title block in a RichMessage. | Bot API 10.2 |
| [`RichBlockSubtitle`](https://core.telegram.org/bots/api#richblocksubtitle) | Subtitle block in a RichMessage. | Bot API 10.2 |
| [`RichBlockAuthorDate`](https://core.telegram.org/bots/api#richblockauthordate) | Author and publication date block in a RichMessage. | Bot API 10.2 |
| [`RichBlockHeader`](https://core.telegram.org/bots/api#richblockheader) | Section header block in a RichMessage. | Bot API 10.2 |
| [`RichBlockSubheader`](https://core.telegram.org/bots/api#richblocksubheader) | Section subheader block in a RichMessage. | Bot API 10.2 |
| [`RichBlockParagraph`](https://core.telegram.org/bots/api#richblockparagraph) | Paragraph block in a RichMessage. | Bot API 10.2 |
| [`RichBlockPreformatted`](https://core.telegram.org/bots/api#richblockpreformatted) | Preformatted/code block in a RichMessage. | Bot API 10.2 |
| [`RichBlockFooter`](https://core.telegram.org/bots/api#richblockfooter) | Footer block in a RichMessage. | Bot API 10.2 |
| [`RichBlockDivider`](https://core.telegram.org/bots/api#richblockdivider) | Horizontal rule divider block in a RichMessage. | Bot API 10.2 |
| [`RichBlockAnchor`](https://core.telegram.org/bots/api#richblockanchor) | Named anchor target block in a RichMessage. | Bot API 10.2 |
| [`RichBlockList`](https://core.telegram.org/bots/api#richblocklist) | Ordered or unordered list block in a RichMessage. | Bot API 10.2 |
| [`RichBlockBlockquote`](https://core.telegram.org/bots/api#richblockblockquote) | Blockquote block in a RichMessage. | Bot API 10.2 |
| [`RichBlockPullquote`](https://core.telegram.org/bots/api#richblockpullquote) | Pullquote block in a RichMessage. | Bot API 10.2 |
| [`RichBlockPhoto`](https://core.telegram.org/bots/api#richblockphoto) | Photo block in a RichMessage. | Bot API 10.2 |
| [`RichBlockVideo`](https://core.telegram.org/bots/api#richblockvideo) | Video block in a RichMessage. | Bot API 10.2 |
| [`RichBlockAnimation`](https://core.telegram.org/bots/api#richblockanimation) | Animation block in a RichMessage. | Bot API 10.2 |
| [`RichBlockAudio`](https://core.telegram.org/bots/api#richblockaudio) | Audio block in a RichMessage. | Bot API 10.2 |
| [`RichBlockVoice`](https://core.telegram.org/bots/api#richblockvoice) | Voice block in a RichMessage. | Bot API 10.2 |
| [`RichBlockDocument`](https://core.telegram.org/bots/api#richblockdocument) | Document block in a RichMessage. | Bot API 10.2 |
| [`RichBlockLocation`](https://core.telegram.org/bots/api#richblocklocation) | Location map block in a RichMessage. | Bot API 10.2 |
| [`RichBlockSlideshow`](https://core.telegram.org/bots/api#richblockslideshow) | Media slideshow block in a RichMessage. | Bot API 10.2 |
| [`RichBlockCollage`](https://core.telegram.org/bots/api#richblockcollage) | Media collage grid block in a RichMessage. | Bot API 10.2 |
| [`RichBlockEmbedPost`](https://core.telegram.org/bots/api#richblockembedpost) | Embedded Telegram post block in a RichMessage. | Bot API 10.2 |
| [`RichBlockTable`](https://core.telegram.org/bots/api#richblocktable) | Structured table block in a RichMessage. | Bot API 10.2 |
| [`RichBlockDetails`](https://core.telegram.org/bots/api#richblockdetails) | Collapsible details/accordion block in a RichMessage. | Bot API 10.2 |
| [`RichBlockRelatedArticles`](https://core.telegram.org/bots/api#richblockrelatedarticles) | Related articles links block in a RichMessage. | Bot API 10.2 |
| [`InputRichBlockListItem`](https://core.telegram.org/bots/api#inputrichblocklistitem) | Input item for an InputRichBlockList. | Bot API 10.2 |
| [`InputRichBlock`](https://core.telegram.org/bots/api#inputrichblock) | Union of 25 InputRichBlock* structural block types for sendRichMessage. | Bot API 10.2 |
| [`InputRichBlockTitle`](https://core.telegram.org/bots/api#inputrichblocktitle) | Input title block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockSubtitle`](https://core.telegram.org/bots/api#inputrichblocksubtitle) | Input subtitle block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockAuthorDate`](https://core.telegram.org/bots/api#inputrichblockauthordate) | Input author/date block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockHeader`](https://core.telegram.org/bots/api#inputrichblockheader) | Input header block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockSubheader`](https://core.telegram.org/bots/api#inputrichblocksubheader) | Input subheader block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockParagraph`](https://core.telegram.org/bots/api#inputrichblockparagraph) | Input paragraph block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockPreformatted`](https://core.telegram.org/bots/api#inputrichblockpreformatted) | Input preformatted/code block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockFooter`](https://core.telegram.org/bots/api#inputrichblockfooter) | Input footer block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockDivider`](https://core.telegram.org/bots/api#inputrichblockdivider) | Input divider block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockAnchor`](https://core.telegram.org/bots/api#inputrichblockanchor) | Input anchor block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockList`](https://core.telegram.org/bots/api#inputrichblocklist) | Input list block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockBlockquote`](https://core.telegram.org/bots/api#inputrichblockblockquote) | Input blockquote block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockPullquote`](https://core.telegram.org/bots/api#inputrichblockpullquote) | Input pullquote block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockPhoto`](https://core.telegram.org/bots/api#inputrichblockphoto) | Input photo block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockVideo`](https://core.telegram.org/bots/api#inputrichblockvideo) | Input video block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockAnimation`](https://core.telegram.org/bots/api#inputrichblockanimation) | Input animation block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockAudio`](https://core.telegram.org/bots/api#inputrichblockaudio) | Input audio block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockVoice`](https://core.telegram.org/bots/api#inputrichblockvoice) | Input voice block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockDocument`](https://core.telegram.org/bots/api#inputrichblockdocument) | Input document block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockLocation`](https://core.telegram.org/bots/api#inputrichblocklocation) | Input location block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockSlideshow`](https://core.telegram.org/bots/api#inputrichblockslideshow) | Input slideshow block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockCollage`](https://core.telegram.org/bots/api#inputrichblockcollage) | Input collage block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockEmbedPost`](https://core.telegram.org/bots/api#inputrichblockembedpost) | Input embedded post block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockTable`](https://core.telegram.org/bots/api#inputrichblocktable) | Input table block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockDetails`](https://core.telegram.org/bots/api#inputrichblockdetails) | Input collapsible details block for InputRichMessage. | Bot API 10.2 |
| [`InputRichBlockRelatedArticles`](https://core.telegram.org/bots/api#inputrichblockrelatedarticles) | Input related articles block for InputRichMessage. | Bot API 10.2 |

## Inline Mode (34)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`InlineQuery`](https://core.telegram.org/bots/api#inlinequery) | Represents an incoming inline query. | Bot API 1.0 |
| [`InlineQueryResultsButton`](https://core.telegram.org/bots/api#inlinequeryresultsbutton) | Represents a button to be shown above inline query results. | Bot API 6.7 |
| [`InlineQueryResult`](https://core.telegram.org/bots/api#inlinequeryresult) | Union of 20 InlineQueryResult* types. | Bot API 1.0 |
| [`InlineQueryResultArticle`](https://core.telegram.org/bots/api#inlinequeryresultarticle) | Represents a link to an article or web page. | Bot API 1.0 |
| [`InlineQueryResultPhoto`](https://core.telegram.org/bots/api#inlinequeryresultphoto) | Represents a link to a photo. | Bot API 1.0 |
| [`InlineQueryResultGif`](https://core.telegram.org/bots/api#inlinequeryresultgif) | Represents a link to an animated GIF file. | Bot API 1.0 |
| [`InlineQueryResultMpeg4Gif`](https://core.telegram.org/bots/api#inlinequeryresultmpeg4gif) | Represents a link to a video animation (H.264/MPEG-4 AVC video without sound). | Bot API 1.0 |
| [`InlineQueryResultVideo`](https://core.telegram.org/bots/api#inlinequeryresultvideo) | Represents a link to a page containing an embedded video player or a video file. | Bot API 1.0 |
| [`InlineQueryResultAudio`](https://core.telegram.org/bots/api#inlinequeryresultaudio) | Represents a link to an MP3 audio file. | Bot API 2.0 |
| [`InlineQueryResultVoice`](https://core.telegram.org/bots/api#inlinequeryresultvoice) | Represents a link to a voice recording in an .OGG container encoded with OPUS. | Bot API 2.0 |
| [`InlineQueryResultDocument`](https://core.telegram.org/bots/api#inlinequeryresultdocument) | Represents a link to a file. | Bot API 2.0 |
| [`InlineQueryResultLocation`](https://core.telegram.org/bots/api#inlinequeryresultlocation) | Represents a location on a map. | Bot API 2.0 |
| [`InlineQueryResultVenue`](https://core.telegram.org/bots/api#inlinequeryresultvenue) | Represents a venue. | Bot API 2.0 |
| [`InlineQueryResultContact`](https://core.telegram.org/bots/api#inlinequeryresultcontact) | Represents a contact with a phone number. | Bot API 2.0 |
| [`InlineQueryResultGame`](https://core.telegram.org/bots/api#inlinequeryresultgame) | Represents a Game. | Bot API 2.2 |
| [`InlineQueryResultCachedPhoto`](https://core.telegram.org/bots/api#inlinequeryresultcachedphoto) | Represents a link to a photo stored on the Telegram servers. | Bot API 2.0 |
| [`InlineQueryResultCachedGif`](https://core.telegram.org/bots/api#inlinequeryresultcachedgif) | Represents a link to an animated GIF file stored on the Telegram servers. | Bot API 2.0 |
| [`InlineQueryResultCachedMpeg4Gif`](https://core.telegram.org/bots/api#inlinequeryresultcachedmpeg4gif) | Represents a link to a video animation stored on the Telegram servers. | Bot API 2.0 |
| [`InlineQueryResultCachedSticker`](https://core.telegram.org/bots/api#inlinequeryresultcachedsticker) | Represents a link to a sticker stored on the Telegram servers. | Bot API 2.0 |
| [`InlineQueryResultCachedDocument`](https://core.telegram.org/bots/api#inlinequeryresultcacheddocument) | Represents a link to a file stored on the Telegram servers. | Bot API 2.0 |
| [`InlineQueryResultCachedVideo`](https://core.telegram.org/bots/api#inlinequeryresultcachedvideo) | Represents a link to a video file stored on the Telegram servers. | Bot API 2.0 |
| [`InlineQueryResultCachedVoice`](https://core.telegram.org/bots/api#inlinequeryresultcachedvoice) | Represents a link to a voice message stored on the Telegram servers. | Bot API 2.0 |
| [`InlineQueryResultCachedAudio`](https://core.telegram.org/bots/api#inlinequeryresultcachedaudio) | Represents a link to an MP3 audio file stored on the Telegram servers. | Bot API 2.0 |
| [`InputMessageContent`](https://core.telegram.org/bots/api#inputmessagecontent) | Union of 7 Input*MessageContent types (including InputWidgetMessageContent & InputSharedWidgetMessageContent in 10.4). | Bot API 2.0 (updated 10.4) |
| [`InputTextMessageContent`](https://core.telegram.org/bots/api#inputtextmessagecontent) | Represents the content of a text message to be sent as the result of an inline query. | Bot API 2.0 |
| [`InputLocationMessageContent`](https://core.telegram.org/bots/api#inputlocationmessagecontent) | Represents the content of a location message to be sent as the result of an inline query. | Bot API 2.0 |
| [`InputVenueMessageContent`](https://core.telegram.org/bots/api#inputvenuemessagecontent) | Represents the content of a venue message to be sent as the result of an inline query. | Bot API 2.0 |
| [`InputContactMessageContent`](https://core.telegram.org/bots/api#inputcontactmessagecontent) | Represents the content of a contact message to be sent as the result of an inline query. | Bot API 2.0 |
| [`InputInvoiceMessageContent`](https://core.telegram.org/bots/api#inputinvoicemessagecontent) | Represents the content of an invoice message to be sent as the result of an inline query. | Bot API 5.2 |
| [`InputWidgetMessageContent`](https://core.telegram.org/bots/api#inputwidgetmessagecontent) | Represents the content of an in-chat Widget message to be sent as the result of an inline query. | Bot API 10.4 |
| [`InputSharedWidgetMessageContent`](https://core.telegram.org/bots/api#inputsharedwidgetmessagecontent) | Represents the content of an in-chat SharedWidget message to be sent as the result of an inline query. | Bot API 10.4 |
| [`ChosenInlineResult`](https://core.telegram.org/bots/api#choseninlineresult) | Represents a result of an inline query that was chosen by the user and sent to their chat partner. | Bot API 1.0 |
| [`SentWebAppMessage`](https://core.telegram.org/bots/api#sentwebappmessage) | Describes an inline message sent by a Web App on behalf of a user. | Bot API 6.0 |
| [`PreparedInlineMessage`](https://core.telegram.org/bots/api#preparedinlinemessage) | Describes an inline message to be sent by a user of a Mini App (id, expiration_date). | Bot API 8.0 |

## Payments, Stars & Affiliates (25)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`LabeledPrice`](https://core.telegram.org/bots/api#labeledprice) | Represents a portion of the price for goods or services (label, amount). | Bot API 3.0 |
| [`Invoice`](https://core.telegram.org/bots/api#invoice) | Contains basic information about an invoice. | Bot API 3.0 |
| [`ShippingAddress`](https://core.telegram.org/bots/api#shippingaddress) | Represents a shipping address. | Bot API 3.0 |
| [`OrderInfo`](https://core.telegram.org/bots/api#orderinfo) | Represents information about an order. | Bot API 3.0 |
| [`ShippingOption`](https://core.telegram.org/bots/api#shippingoption) | Represents one shipping option. | Bot API 3.0 |
| [`SuccessfulPayment`](https://core.telegram.org/bots/api#successfulpayment) | Contains basic information about a successful payment (includes subscription_expiration_date, is_recurring, is_first_recurring, telegram_payment_charge_id). | Bot API 3.0 (updated 8.0) |
| [`RefundedPayment`](https://core.telegram.org/bots/api#refundedpayment) | Contains basic information about a refunded payment. | Bot API 7.7 |
| [`ShippingQuery`](https://core.telegram.org/bots/api#shippingquery) | Contains information about an incoming shipping query. | Bot API 3.0 |
| [`PreCheckoutQuery`](https://core.telegram.org/bots/api#precheckoutquery) | Contains information about an incoming pre-checkout query. | Bot API 3.0 |
| [`PaidMediaPurchased`](https://core.telegram.org/bots/api#paidmediapurchased) | Contains information about a paid media purchase (from, paid_media_payload). | Bot API 7.9 |
| [`RevenueWithdrawalState`](https://core.telegram.org/bots/api#revenuewithdrawalstate) | Union of RevenueWithdrawalStatePending | RevenueWithdrawalStateSucceeded | RevenueWithdrawalStateFailed. | Bot API 7.4 |
| [`RevenueWithdrawalStatePending`](https://core.telegram.org/bots/api#revenuewithdrawalstatepending) | The withdrawal is in progress. | Bot API 7.4 |
| [`RevenueWithdrawalStateSucceeded`](https://core.telegram.org/bots/api#revenuewithdrawalstatesucceeded) | The withdrawal succeeded (date, url). | Bot API 7.4 |
| [`RevenueWithdrawalStateFailed`](https://core.telegram.org/bots/api#revenuewithdrawalstatefailed) | The withdrawal failed and the balance was refunded. | Bot API 7.4 |
| [`AffiliateInfo`](https://core.telegram.org/bots/api#affiliateinfo) | Contains information about the affiliate that received a commission via this transaction. | Bot API 8.1 |
| [`TransactionPartner`](https://core.telegram.org/bots/api#transactionpartner) | Union of 7 TransactionPartner* types. | Bot API 7.4 (updated 9.1) |
| [`TransactionPartnerUser`](https://core.telegram.org/bots/api#transactionpartneruser) | Describes a transaction with a user (invoice_payload, subscription_period, paid_media, gift, premium_subscription_duration). | Bot API 7.4 (updated 9.0) |
| [`TransactionPartnerChat`](https://core.telegram.org/bots/api#transactionpartnerchat) | Describes a transaction with a chat. | Bot API 8.3 |
| [`TransactionPartnerAffiliateProgram`](https://core.telegram.org/bots/api#transactionpartneraffiliateprogram) | Describes the affiliate program that issued the affiliate commission. | Bot API 8.1 |
| [`TransactionPartnerFragment`](https://core.telegram.org/bots/api#transactionpartnerfragment) | Describes a withdrawal transaction with Fragment. | Bot API 7.4 |
| [`TransactionPartnerTelegramAds`](https://core.telegram.org/bots/api#transactionpartnertelegramads) | Describes a withdrawal transaction to the Telegram Ads platform. | Bot API 7.4 |
| [`TransactionPartnerTelegramApi`](https://core.telegram.org/bots/api#transactionpartnertelegramapi) | Describes a transaction with payment for paid broadcasting. | Bot API 7.11 |
| [`TransactionPartnerOther`](https://core.telegram.org/bots/api#transactionpartnerother) | Describes a transaction with an unknown source or recipient. | Bot API 7.4 |
| [`StarTransaction`](https://core.telegram.org/bots/api#startransaction) | Describes a Telegram Star transaction (id, amount, nanostar_amount, date, source, receiver). | Bot API 7.4 (updated 8.1) |
| [`StarTransactions`](https://core.telegram.org/bots/api#startransactions) | Contains a list of Telegram Star transactions. | Bot API 7.4 |

## Telegram Passport (14)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`PassportData`](https://core.telegram.org/bots/api#passportdata) | Describes Telegram Passport data shared with the bot by the user. | Bot API 4.0 |
| [`PassportFile`](https://core.telegram.org/bots/api#passportfile) | Represents a file uploaded to Telegram Passport. | Bot API 4.0 |
| [`EncryptedPassportElement`](https://core.telegram.org/bots/api#encryptedpassportelement) | Describes documents or other Telegram Passport elements shared with the bot by the user. | Bot API 4.0 |
| [`EncryptedCredentials`](https://core.telegram.org/bots/api#encryptedcredentials) | Describes data required for decrypting and authenticating EncryptedPassportElement. | Bot API 4.0 |
| [`PassportElementError`](https://core.telegram.org/bots/api#passportelementerror) | Union of 8 PassportElementError* types. | Bot API 4.0 |
| [`PassportElementErrorDataField`](https://core.telegram.org/bots/api#passportelementerrordatafield) | Represents an issue in one of the data fields that was provided by the user. | Bot API 4.0 |
| [`PassportElementErrorFrontSide`](https://core.telegram.org/bots/api#passportelementerrorfrontside) | Represents an issue with the front side of a document. | Bot API 4.0 |
| [`PassportElementErrorReverseSide`](https://core.telegram.org/bots/api#passportelementerrorreverseside) | Represents an issue with the reverse side of a document. | Bot API 4.0 |
| [`PassportElementErrorSelfie`](https://core.telegram.org/bots/api#passportelementerrorselfie) | Represents an issue with the selfie with a document. | Bot API 4.0 |
| [`PassportElementErrorFile`](https://core.telegram.org/bots/api#passportelementerrorfile) | Represents an issue with a document scan. | Bot API 4.0 |
| [`PassportElementErrorFiles`](https://core.telegram.org/bots/api#passportelementerrorfiles) | Represents an issue with a list of scans. | Bot API 4.0 |
| [`PassportElementErrorTranslationFile`](https://core.telegram.org/bots/api#passportelementerrortranslationfile) | Represents an issue with one of the files that constitute the translation of a document. | Bot API 4.0 |
| [`PassportElementErrorTranslationFiles`](https://core.telegram.org/bots/api#passportelementerrortranslationfiles) | Represents an issue with the translated version of a document. | Bot API 4.0 |
| [`PassportElementErrorUnspecified`](https://core.telegram.org/bots/api#passportelementerrorunspecified) | Represents an issue in an unspecified place. | Bot API 4.0 |

## Games (3)

| Type | Description & Key Fields | Introduced / Updated |
|---|---|---|
| [`Game`](https://core.telegram.org/bots/api#game) | Represents a game. | Bot API 2.2 |
| [`CallbackGame`](https://core.telegram.org/bots/api#callbackgame) | A placeholder, currently holds no information. Use BotFather to set up your game. | Bot API 2.2 |
| [`GameHighScore`](https://core.telegram.org/bots/api#gamehighscore) | Represents one row of the high scores table for a game. | Bot API 2.2 |
