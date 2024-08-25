// site/DocumentsPage/index.tsx
import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Layout from "@/components/Layout";
import Icon from "@/components/Icon";
import { documentOptions } from "@/constants/document-options";
import HorizontalMenu from "@/components/HorizontalMenu";
import TagList from "@/components/TagList";
import Card from "@/components/Card";
import DocumentDetailPage from "@/site/DocumentDetailPage";
import { DocumentType } from "@/types/DocumentType";
import { API_ENDPOINTS } from "@/utils/apiConfig";
import axios from "axios";
import { Tag } from '@/site/ViewAllTagsPage';

const DocumentsPage = () => {
    const [search, setSearch] = useState<string>("");
    const router = useRouter();
    const { id } = router.query;
    const [document, setDocument] = useState<DocumentType | null>(null);
    const [documents, setDocuments] = useState<DocumentType[]>([]);
    const [tags, setTags] = useState<string[]>([]);

    const getRandomTags = (tags: Tag[], count: number): Tag[] => {
        const shuffled = tags.sort(() => 0.5 - Math.random());
        return shuffled.slice(0, count);
    };

    useEffect(() => {
        if (id) {
            const doc = documents.find((doc) => doc.id === id);
            setDocument(doc || null);
        }
    }, [id, documents]);

    useEffect(() => {
        const fetchDocuments = async () => {
            try {
                const response = await axios.get(API_ENDPOINTS.GET_DOCUMENT);
                setDocuments(response.data);
            } catch (error) {
                console.error('Error fetching documents:', error);
            }
        };

        const fetchTags = async () => {
            try {
                const response = await axios.get(API_ENDPOINTS.TAGS);
                const randomTags = getRandomTags(response.data, 6);
                const tagNames = randomTags.map(tag => tag.name === '-1' ? 'DOC_NO_TAGS' : tag.name);
                setTags(tagNames);
            } catch (error) {
                console.error('Error fetching tags:', error);
            }
        };

        fetchDocuments();
        fetchTags();
    }, []);

    if (id && document) {
        return <DocumentDetailPage document={document} />;
    }

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
                    Documents
                </div>
                <div className="mb-8 body1 text-n-4 md:mb-6 md:body1S">
                    Manage and organize your documents with ease
                </div>
                <div className="mb-8 body1 text-n-4 md:mb-6 md:body1S">
                    <HorizontalMenu
                        className="shrink-0 w-[27.875rem] lg:w-full lg:mt-10"
                        items={documentOptions}
                    />
                </div>
                <TagList tags={tags}/> {/* Update to use fetched random tags */}
                <div className="mb-2 h6 text-n-4 md:mb-6">Your Documents</div>
                <div className="flex flex-wrap -mx-4">
                    {documents.map((doc, index) => (
                        <Card key={index} document={doc}/>
                    ))}
                </div>
            </div>
        </Layout>
    );
};

export default DocumentsPage;