import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import axios from "axios";

// Create an MCP server
const server = new McpServer({
    name: "Demo",
    version: "1.0.0"
});

server.tool("add",
    { a: z.number(), b: z.number() },
    async ({ a, b }) => {
        const sum = a + b;
        return { content: [{ type: "text", text: sum }] }
    }
);

server.tool(
    'weather',
    { city: z.string().describe('Name of the city') },
    async ({ city }) => {
        const response = await axios.get(`https://wttr.in/${city}?format=%C+%t`, {
            responseType: 'json',
        });
        return { content: [{ type: 'text', text: JSON.stringify(response.data) }] };
    }
);

const transport = new StdioServerTransport();
await server.connect(transport);
