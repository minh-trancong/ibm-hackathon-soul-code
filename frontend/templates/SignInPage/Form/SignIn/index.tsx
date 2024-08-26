import React, { useState } from "react";
import { useRouter } from 'next/router';
import Field from "@/components/Field";
import { signIn } from '@/utils/auth';

type SignInProps = {
    onClick: () => void;
};

const SignIn = ({ onClick }: SignInProps) => {
    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [error, setError] = useState<string>("");
    const router = useRouter();

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const success = await signIn(username, password);
        if (success) {
            router.push('/').then(() => {
                console.log("ok");
            });
        } else {
            setError('Invalid username or password');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <Field
                className="mb-4"
                classInput="dark:bg-n-7 dark:border-n-7 dark:focus:bg-transparent"
                placeholder="Username or email"
                icon="email"
                value={username}
                onChange={(e: any) => setUsername(e.target.value)}
                required
            />
            <Field
                className="mb-2"
                classInput="dark:bg-n-7 dark:border-n-7 dark:focus:bg-transparent"
                placeholder="Password"
                icon="lock"
                type="password"
                value={password}
                onChange={(e: any) => setPassword(e.target.value)}
                required
            />
            <button
                className="mb-6 base2 text-primary-1 transition-colors hover:text-primary-1/90"
                type="button"
                onClick={onClick}
            >
                Forgot password?
            </button>
            {error && <p>{error}</p>}
            <button className="btn-blue btn-large w-full" type="submit">
                Sign in with SoulCode
            </button>
        </form>
    );
};

export default SignIn;