import React from "react";
import {EditorContent, useEditor} from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import Bold from "@tiptap/extension-bold";
import Italic from "@tiptap/extension-italic";
import Heading from "@tiptap/extension-heading";
import BulletList from "@tiptap/extension-bullet-list";
import OrderedList from "@tiptap/extension-ordered-list";
import ListItem from "@tiptap/extension-list-item";
import Blockquote from "@tiptap/extension-blockquote";
import CodeBlock from "@tiptap/extension-code-block";
import {useRouter} from "next/router";
import Layout from "@/components/Layout";
import Icon from "@/components/Icon";
import TurndownService from "turndown";
import {Node} from 'domhandler';
import {API_ENDPOINTS} from '@/utils/apiConfig';
import axios from "axios";

const WriteNotePage = () => {
    const editor = useEditor({
        extensions: [
            StarterKit,
            Bold,
            Italic,
            Heading.configure({levels: [1, 2, 3]}),
            BulletList,
            OrderedList,
            ListItem,
            Blockquote,
            CodeBlock,
        ],
        content: "",
    });
    const router = useRouter();
    const turndownService = new TurndownService();

    turndownService.addRule('heading', {
        filter: ['h1', 'h2', 'h3'],
        replacement: function (content: string, node: Node, options: any) {
            const hLevel = (node as unknown as HTMLElement).nodeName.charAt(1);
            return `${'#'.repeat(parseInt(hLevel))} ${content}\n\n`;
        }
    });

    const handleSave = async () => {
        if (!editor) return;
        const html = editor.getHTML();
        const markdown = turndownService.turndown(html);

        const formData = new FormData();
        formData.append('user_id', '5f5e6c37-b453-4686-8742-5c6e223153a7');
        formData.append('title', 'Untitled Note');
        formData.append('file', new Blob([markdown], {type: 'text/markdown'}));

        try {
            const response = await axios.post(API_ENDPOINTS.UPLOAD_DOCUMENT, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            alert('Document uploaded successfully:' + response.data);
        } catch (error) {
            if (axios.isAxiosError(error) && error.response) {
                alert('Error uploading document:' + error.response.data);
            } else {
                alert('Error uploading document:' + error);
            }
        }
    };

    return (
        <Layout hideRightSidebar>
            <div className="p-10 md:pt-5 md:px-6 md:pb-10">
                <button
                    className="hidden absolute top-6 right-6 w-10 h-10 border-2 border-n-4/25 rounded-full text-0 transition-colors hover:border-transparent hover:bg-n-4/25 md:block"
                    onClick={() => router.back()}
                >
                    <Icon className="fill-n-4" name="close"/>
                </button>
                <div className="h3 leading-[4rem] md:mb-3 md:h3">
                    Write Note
                </div>
                <div className="mb-8 body1 text-n-4 md:mb-6 md:body1S">
                    Use the editor below to write your note.
                </div>
                <div className="toolbar mb-4 flex space-x-2">
                    <button className="toolbar-button"
                            onClick={() => editor && editor.chain().focus().toggleBold().run()}>Bold
                    </button>
                    <button className="toolbar-button"
                            onClick={() => editor && editor.chain().focus().toggleItalic().run()}>Italic
                    </button>
                    <button className="toolbar-button"
                            onClick={() => editor && editor.chain().focus().toggleHeading({level: 1}).run()}>H1
                    </button>
                    <button className="toolbar-button"
                            onClick={() => editor && editor.chain().focus().toggleHeading({level: 2}).run()}>H2
                    </button>
                    <button className="toolbar-button"
                            onClick={() => editor && editor.chain().focus().toggleHeading({level: 3}).run()}>H3
                    </button>
                    <button className="toolbar-button"
                            onClick={() => editor && editor.chain().focus().toggleBulletList().run()}>Bullet List
                    </button>
                    <button className="toolbar-button"
                            onClick={() => editor && editor.chain().focus().toggleOrderedList().run()}>Ordered List
                    </button>
                    <button className="toolbar-button"
                            onClick={() => editor && editor.chain().focus().toggleBlockquote().run()}>Blockquote
                    </button>
                    <button className="toolbar-button"
                            onClick={() => editor && editor.chain().focus().toggleCodeBlock().run()}>Code Block
                    </button>
                </div>
                <EditorContent editor={editor} className="border p-4 mb-6"/>
                <button
                    onClick={handleSave}
                    className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
                >
                    Save
                </button>
            </div>
        </Layout>
    );
};

export default WriteNotePage;