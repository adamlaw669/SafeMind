
type PropType = {
    className?: string
}
const CompanyName = ({ className }: PropType) => {
    return (
        // Add custom style with "className" prop
        <h1 className={` ${className}`}>Safe<span className="text-primaryBlue-300">Mind</span></h1>
    )
}

export default CompanyName