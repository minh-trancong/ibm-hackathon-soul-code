// frontend/site/DocumentDetailPage/index.tsx
import React, {useRef} from "react";
import Layout from "@/components/Layout";
import html2canvas from "html2canvas";
import TagList from "@/components/TagList";

type DocumentType = {
    id: string;
    image: string;
    title: string;
    summary: string;
    tags: string[];
};

type DocumentDetailPageProps = {
    document: DocumentType;
};

const DocumentDetailPage = ({document}: DocumentDetailPageProps) => {
    const pageRef = useRef<HTMLDivElement>(null);

    const captureThumbnail = async () => {
        if (pageRef.current) {
            const canvas = await html2canvas(pageRef.current);
            const imgData = canvas.toDataURL("image/png");

            // Create a link element
            const link = window.document.createElement("a");
            link.href = imgData;
            link.download = "thumbnail.png";

            // Programmatically click the link to trigger the download
            link.click();

            // Remove the link element
            link.remove();
        }
    };

    return (
        <Layout showRelatedDocumentSideBar smallSidebar>
            <div className="p-10 md:pt-5 md:px-6 md:pb-10 min-h-screen flex flex-col">
                <div ref={pageRef}>
                    <h1>{document.title}</h1>
                    <p className="bg-blue-100 border border-blue-500 text-blue-700 p-4">
                        <h2>Summary</h2>
                        {document.summary}
                        <TagList tags={document.tags} hideViewAll/>
                    </p>
                </div>
                <div className="mt-auto">
                    <button
                        className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors"
                        onClick={captureThumbnail}
                    >
                        Update Thumbnail
                    </button>
                </div>
            </div>
        </Layout>
    );
};

export default DocumentDetailPage;