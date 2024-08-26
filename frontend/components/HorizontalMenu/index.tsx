import Link from "next/link";
import Icon from "@/components/Icon";

type MenuType = {
    title: string;
    icon: string;
    color: string;
    url: string;
};

type HorizontalMenuProps = {
    className?: string;
    items: MenuType[];
};

const HorizontalMenu = ({ className, items }: HorizontalMenuProps) => (
    <div className={`grid grid-cols-3 gap-4 w-full max-w-5xl ${className}`}>
        {items.map((item, index) => (
            <Link
                className="group flex items-center p-2 border border-n-3 rounded-lg text-sm transition-all hover:border-transparent hover:shadow-[0_0_0.5rem_0.125rem_rgba(0,0,0,0.04),0px_1rem_0.75rem_-0.5rem_rgba(0,0,0,0.12)] dark:border-n-5 dark:hover:border-n-7 dark:hover:bg-n-7"
                href={item.url}
                key={index}
            >
                <div className="relative flex justify-center items-center w-10 h-10 mr-4">
                    <div
                        className="absolute inset-0 opacity-20 rounded-lg"
                        style={{
                            backgroundColor: item.color,
                        }}
                    ></div>
                    <Icon
                        className="relative z-1"
                        fill={item.color}
                        name={item.icon}
                    />
                </div>
                {item.title}
                <Icon
                    className="ml-auto fill-n-4 transition-colors group-hover:fill-n-7 dark:group-hover:fill-n-4"
                    name="arrow-next"
                />
            </Link>
        ))}
    </div>
);

export default HorizontalMenu;