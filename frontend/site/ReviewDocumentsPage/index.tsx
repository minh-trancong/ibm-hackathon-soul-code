import { useState } from "react";
import { useRouter } from "next/router";
import Layout from "@/components/Layout";
import Icon from "@/components/Icon";
import HorizontalMenu from "@/components/HorizontalMenu";
import Card from "@/components/Card";
import { documents } from "@/mocks/documents"; // Import the documents data
import { reviewOptions } from "@/constants/review-options";

const ReviewDocumentsPage = () => {
    const [search, setSearch] = useState<string>("");
    const router = useRouter();

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
                    Master Your Material
                </div>
                <div className="mb-8 body1 text-n-4 md:mb-6 md:body1S">
                    Spaced Repetition and Active Recall to enhance your learning efficiency
                </div>
                <div className="mb-2 h6 text-n-4 md:mb-6">Active Recall</div>
                <div className="mb-8 body1 text-n-4 md:mb-6 md:body1S">
                    <HorizontalMenu
                        className="shrink-0 w-[27.875rem] lg:w-full lg:mt-10"
                        items={reviewOptions}
                    />
                </div>
                <div className="mb-2 h6 text-n-4 md:mb-6">Spaced Repetition Review Documents</div>
                <div className="flex flex-wrap -mx-4">
                    {documents.map((doc, index) => (
                        <Card key={index} document={doc}/>
                    ))}
                </div>
            </div>
        </Layout>
    );
};

export default ReviewDocumentsPage;