import Link from "next/link";
import Image from "@/components/Image";

type TestProps = {
    className?: string;
    dark?: boolean;
};

const Test = ({ className, dark }: TestProps) => (
    <Link className={`flex w-[11.88rem] ${className}`} href="/">
        <Image
            className="w-full h-auto"
            src={dark ? "/logos/soulcode-logo-main.png" : "/logos/soulcode-logo-main-dark.png"}
            width={190}
            height={40}
            alt="SoulCode"
        />
    </Link>
);

export default Test;
