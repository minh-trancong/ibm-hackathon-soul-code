// frontend/mocks/documents.tsx
import { DocumentType } from "@/types/DocumentType";

export const documents: DocumentType[] = [
    {
        id: "1",
        image: "/images/video-pic.jpg",
        title: "Document Title 1",
        summary: "This is a summary of the document 1.",
        tags: ["tag1", "tag2", "tag3"],
    },
    {
        id: "2",
        image: "/icons/activity.svg",
        title: "Document Title 2",
        summary: "This is a summary of the document 2.",
        tags: ["tag1", "tag2", "tag3"],
    },
];