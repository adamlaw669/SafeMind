import type { ReactElement } from "react"

type ActionButtonProps = {
    icon?: ReactElement;
    type?: "submit" | "reset" | "button" | undefined
    children:ReactElement;
    className?: string;
    onClick?: ()=>void;
    disabled?: boolean
}

const ActionButton = ({children, type, className, onClick, disabled} : ActionButtonProps) => {
  return (
    <button type={type} className={`${className} w-fit rounded-full px-3 py-2 cursor-pointer font-semibold text-center flex flex-row justify-center items-center hover:transition-all hover:duration-200m disabled:bg-[#A5A5A5] disabled:cursor-not-allowed`} onClick={onClick} disabled={disabled}>
        {children}
    </button>
  )
}

export default ActionButton