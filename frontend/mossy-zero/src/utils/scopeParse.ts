type AccessPermission = {
    scope: string;
    description: string;
    children?: AccessPermission[];
};

const scopeDescriptions: Record<string, AccessPermission> = {
    read: {
        scope: "read", description: "Grants access to read data.", children: [
            { scope: "read:accounts", description: "Read accounts" },
            { scope: "read:blocks", description: "Read blocks" },
            { scope: "read:bookmarks", description: "Read bookmarks" },
            { scope: "read:favourites", description: "Read favourites" },
            { scope: "read:filters", description: "Read filters" },
            { scope: "read:follows", description: "Read follows" },
            { scope: "read:lists", description: "Read lists" },
            { scope: "read:mutes", description: "Read mutes" },
            { scope: "read:notifications", description: "Read notifications" },
            { scope: "read:search", description: "Read search" },
            { scope: "read:statuses", description: "Read statuses" }
        ]
    },
    write: {
        scope: "write", description: "Grants access to write data.", children: [
            { scope: "write:accounts", description: "Write accounts" },
            { scope: "write:blocks", description: "Write blocks" },
            { scope: "write:bookmarks", description: "Write bookmarks" },
            { scope: "write:conversations", description: "Write conversations" },
            { scope: "write:favourites", description: "Write favourites" },
            { scope: "write:filters", description: "Write filters" },
            { scope: "write:follows", description: "Write follows" },
            { scope: "write:lists", description: "Write lists" },
            { scope: "write:media", description: "Write media" },
            { scope: "write:mutes", description: "Write mutes" },
            { scope: "write:notifications", description: "Write notifications" },
            { scope: "write:reports", description: "Write reports" },
            { scope: "write:statuses", description: "Write statuses" }
        ]
    },
    push: { scope: "push", description: "Grants access to Web Push API subscriptions." },
    admin: {
        scope: "admin", description: "Admin scopes", children: [
            {
                scope: "admin:read", description: "Admin read", children: [
                    { scope: "admin:read:accounts", description: "Admin read accounts" },
                    { scope: "admin:read:reports", description: "Admin read reports" },
                    { scope: "admin:read:domain_allows", description: "Admin read domain allows" },
                    { scope: "admin:read:domain_blocks", description: "Admin read domain blocks" },
                    { scope: "admin:read:ip_blocks", description: "Admin read IP blocks" },
                    { scope: "admin:read:email_domain_blocks", description: "Admin read email domain blocks" },
                    { scope: "admin:read:canonical_email_blocks", description: "Admin read canonical email blocks" },
                ]
            },
            {
                scope: "admin:write", description: "Admin write", children: [
                    { scope: "admin:write:accounts", description: "Admin write accounts" },
                    { scope: "admin:write:reports", description: "Admin write reports" },
                    { scope: "admin:write:domain_allows", description: "Admin write domain allows" },
                    { scope: "admin:write:domain_blocks", description: "Admin write domain blocks" },
                    { scope: "admin:write:ip_blocks", description: "Admin write IP blocks" },
                    { scope: "admin:write:email_domain_blocks", description: "Admin write email domain blocks" },
                    { scope: "admin:write:canonical_email_blocks", description: "Admin write canonical email blocks" },
                ]
            },
        ]
    },
};

function parseOAuthScopes(scopeString: string): AccessPermission[] {
    const scopes = scopeString.split(" ");
    const parsedScopes: AccessPermission[] = [];

    scopes.forEach(scope => {
        const baseScope = scope.split(":")[0];
        if (scopeDescriptions[baseScope]) {
            parsedScopes.push(scopeDescriptions[scope]);
        } else {
            parsedScopes.push({ scope, description: `Unknown scope: ${scope}` });
        }
    });

    return parsedScopes;
}

export default parseOAuthScopes