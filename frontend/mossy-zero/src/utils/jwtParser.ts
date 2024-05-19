// jwtParser.ts

// Function to decode Base64URL
function base64UrlDecode(str: string): string {
    // Replace non-url compatible chars with base64 standard chars
    str = str.replace(/-/g, '+').replace(/_/g, '/');

    // Pad out with standard base64 required padding characters
    switch (str.length % 4) {
        case 0: break;
        case 2: str += '=='; break;
        case 3: str += '='; break;
        default: throw new Error('Invalid base64 string');
    }

    // Base64 decode
    return atob(str);
}

// Define the structure of the JWT parts
interface JwtHeader {
    alg: string;
    typ: string;
}

interface JwtPayload {
    [key: string]: any;
}

interface ParsedJWT {
    header: JwtHeader;
    payload: JwtPayload;
    signature: string;
}

// Function to parse JWT
export function parseJWT(token: string): ParsedJWT {
    const parts = token.split('.');

    if (parts.length !== 3) {
        throw new Error('Invalid JWT token');
    }

    const header = JSON.parse(base64UrlDecode(parts[0]));
    const payload = JSON.parse(base64UrlDecode(parts[1]));
    const signature = parts[2];

    return {
        header: header,
        payload: payload,
        signature: signature
    };
}
