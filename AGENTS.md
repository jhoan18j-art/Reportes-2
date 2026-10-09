<!-- LOVABLE:BEGIN -->
> [!IMPORTANT]
> This project is connected to [Lovable](https://lovable.dev). Avoid rewriting
> published git history — force pushing, or rebasing/amending/squashing commits
> that are already pushed — as it rewrites history on Lovable's side and the
> user will likely lose their project history.
>
> Commits you push to the connected branch sync back to Lovable and show up in
> the editor, so keep the branch in a working state.
<!-- LOVABLE:END -->
- Receipt photo reading runs in a server function (src/lib/receipt.functions.ts) via the AI gateway; photos stored in private 'receipts' bucket under <user_id>/ — keeps keys server-side and files per-user.
- Named accounts (src/lib/catalog.ts USERS) sign in with a synthetic email; accounts and the auditor-viewable password table are created/changed only by server functions in src/lib/accounts.functions.ts — keeps the service-role work server-side.
- Roles live in public.user_roles with has_role(); auditor reads/edits all incomes via RLS — never derive roles from metadata.
