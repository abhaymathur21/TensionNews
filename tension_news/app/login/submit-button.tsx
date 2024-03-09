'use client';

import { useFormStatus } from 'react-dom';
import React, { type ComponentProps } from 'react';
import { type ButtonProps } from '@/components/ui/button';
import { Button } from '@/components/ui/button';

type Props = ButtonProps & {
    pendingText?: string;
    children: React.ReactNode;
};

export function SubmitButton({ children, pendingText, ...props }: Props) {
    const { pending, action } = useFormStatus();

    const isPending = pending && action === props.formAction;

    return (
        <Button {...props} type='submit' aria-disabled={pending}>
            {isPending ? pendingText : children}
        </Button>
    );
}
