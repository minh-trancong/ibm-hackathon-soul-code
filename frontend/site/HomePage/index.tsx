import { useState } from "react";
import { useRouter } from "next/router";
import Layout from "@/components/Layout";
import Icon from "@/components/Icon";
import Home from "./Home";

import { applications } from "@/mocks/applications";

const HomePage = () => {
    const [search, setSearch] = useState<string>("");
    const router = useRouter();

    return (
        <Layout hideRightSidebar>
            <div className="p-10 md:pt-5 md:px-6 md:pb-10">
                <button
                    className="hidden absolute top-6 right-6 w-10 h-10 border-2 border-n-4/25 rounded-full text-0 transition-colors hover:border-transparent hover:bg-n-4/25 md:block"
                    onClick={() => router.back()}
                >
                    <Icon className="fill-n-4" name="close" />
                </button>
                <div className="h3 leading-[4rem] md:mb-3 md:h3">
                    Welcome to SoulCode!
                </div>
                <div className="mb-8 body1 text-n-4 md:mb-6 md:body1S">
                    Manage and organize your Second Brain with SoulCode
                </div>
                <div className="mb-11 h6 text-n-4 md:mb-6">Our features</div>
                <div className="flex flex-wrap -mx-7 -mt-16 2xl:-mx-4 2xl:-mt-12 md:block md:mt-0 md:mx-0">
                    {applications.map((application) => (
                        <Home item={application} key={application.id} />
                    ))}
                </div>
            </div>
        </Layout>
    );
};

export default HomePage;
