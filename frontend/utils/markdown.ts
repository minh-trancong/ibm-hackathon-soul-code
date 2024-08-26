import { Node as ProseMirrorNode } from "prosemirror-model";
import { MarkdownSerializer } from "prosemirror-markdown";
import { defaultMarkdownSerializer } from "prosemirror-markdown";

export const convertToMarkdown = (doc: ProseMirrorNode) => {
    const serializer = new MarkdownSerializer(defaultMarkdownSerializer.nodes, defaultMarkdownSerializer.marks);
    return serializer.serialize(doc);
};