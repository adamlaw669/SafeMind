import type { ReactElement } from "react"

type NeutralButtonProps = {
    icon?: ReactElement;
    type?: "submit" | "reset" | "button" | undefined
    children:ReactElement;
    className?: string;
    onClick?: ()=>void;
}

const NeutralButton = ({children, type, className, onClick} : NeutralButtonProps) => {
  return (
    <button type={type} className={`${className} bg-transparent w-fit rounded-full px-3 py-2 cursor-pointer font-semibold text-center flex flex-row justify-center items-center hover:transition-all hover:duration-200`} onClick={onClick}>
        {children}
    </button>
  )
}

export default NeutralButton