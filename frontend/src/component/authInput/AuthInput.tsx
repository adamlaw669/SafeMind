import type { ReactElement } from "react";


type AuthInputProp = {
    name: string;
    label: string;
    inputType: string;
    placeholder?: string;
    required?: boolean;
    children?: ReactElement
}

const AuthInput = ({name, label, placeholder, inputType, required, children }: AuthInputProp) => {
    return (
        <section className="flex flex-col space-y-2">
            <div className="flex space-x-1">
                <label htmlFor={name}>{label}</label>
                {required && <p className="text-red-600">*</p>}
            </div>
            <div className="border border-black/30 rounded-md px-3 py-2  text-black/80 flex flex-row justify-between items-center w-full">
                <input type={inputType} placeholder={placeholder} required={required} className="w-[90%] outline-none text-lg placeholder:text-black/60 placeholder:text-sm"/>
                {children}
            </div>
        </section>
    )
}

export default AuthInput