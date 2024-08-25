import React, { useEffect } from 'react';
import { useRouter } from 'next/router';
import { isAuthenticated } from '@/utils/auth';
import Layout from "@/components/Layout";
import Main from "./Main";

const HomePage: React.FC = () => {
    const router = useRouter();

    useEffect(() => {
        if (!isAuthenticated()) {
            router.push('/sign-in');
        }
    }, [router]);

    return (
        <Layout hideRightSidebar>
            <Main />
        </Layout>
    );
};

export default HomePage;