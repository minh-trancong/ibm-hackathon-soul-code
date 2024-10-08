// frontend/site/HomePage/Home/index.tsx

import { useRouter } from "next/router";
import Image from "@/components/Image";

type HomeProps = {
    item: any;
};

const Home = ({ item }: HomeProps) => {
    const router = useRouter();

    const handleAccessClick = () => {
        router.push(item.url);
    };

    return (
        <div className="flex flex-col w-[calc(33.333%-3.5rem)] mx-7 mt-16 2xl:w-[calc(33.333%-2rem)] 2xl:mx-4 2xl:mt-12 lg:w-[calc(50%-2rem)] md:w-full md:mx-0 md:mt-10">
            <div className="flex items-center mb-auto">
                <div className="shrink-0 w-15 mr-6">
                    <Image
                        className="w-full rounded-xl"
                        src={item.image}
                        width={60}
                        height={60}
                        alt=""
                    />
                </div>
                <div className="grow">
                    <div className="mb-1 base1 font-semibold">{item.title}</div>
                    <div className="caption1 text-n-4">{item.description}</div>
                </div>
            </div>
            <button className="btn-stroke-light w-full mt-8 md:mt-6" onClick={handleAccessClick}>
                Access
            </button>
        </div>
    );
};

export default Home;