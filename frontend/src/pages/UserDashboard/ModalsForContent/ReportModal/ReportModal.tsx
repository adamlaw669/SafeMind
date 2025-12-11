import { Controller, useForm } from 'react-hook-form';
import SelectFieldComponent from '../../../../component/SelectField/SelectFieldComponent';
import { reportFormValidationSchema, type reportFormValidationSchemaType } from '../../../../schemas/reportFormValidation';
import { zodResolver } from '@hookform/resolvers/zod';
import NeutralButton from '../../../../component/FormButtons/NeutralButton';
import ActionButton from '../../../../component/FormButtons/ActionButton';
import { FaArrowRight } from "react-icons/fa6";
import { useState } from 'react';
import FinalConfirmationModal from './FinalConfirmationModal';


type ReportFormInputsType = {
    name: "category" | "incidentDesc" | "attachFile" | "location";
    label: string
    required: boolean
}

const ReportModal = () => {
    const [openConfirmModal, setOpenConfirmModal] = useState<boolean>(false)
    const [formData, setFormData] = useState<reportFormValidationSchemaType | null>(null)

    const categoryOptions = [
        { value: 'initial', label: 'Select a Category' },
        { value: 'rape', label: 'Rape' },
        { value: 'sexual abuse', label: 'Sexual Abuse' },
        { value: 'violence', label: 'Others' },
    ]

    const reportFormInputs: ReportFormInputsType[] = [
        {
            name: "category",
            label: "Category",
            required: true,
        },
        {
            name: "incidentDesc",
            label: "Incident Description",
            required: true,
        },
        {
            name: "attachFile",
            label: "Attach Supported File",
            required: false,
        },
        {
            name: "location",
            label: "Location",
            required: false,
        },
    ]

    const { register, handleSubmit, control, formState: { errors } } = useForm<reportFormValidationSchemaType>({
        resolver: zodResolver(reportFormValidationSchema)
    })

    const handleReport = (data: reportFormValidationSchemaType) => {
        setOpenConfirmModal(true)

        setFormData(data)
    }

    return (
        <main className="mt-12">
            {openConfirmModal && <FinalConfirmationModal formData={formData}/>}
            <div className="bgImgForReportModal w-[700px] h-[150px] rounded-lg">
                <div className="flex flex-col items-center justify-center space-y-1 h-full">
                    <h1 className="text-[32px] font-semibold">Report Case</h1>
                    <p className="text-[18px] text-black/70">Provide details to help us review your report.</p>
                </div>
            </div>

            <form onSubmit={handleSubmit(handleReport)} className='mt-8 flex flex-col space-y-3'>
                {/* Category Input */}
                {reportFormInputs.map((each, idx) => (
                    <div className='flex flex-col space-y-2' key={idx}>
                        <span className='flex text-[20px]'>
                            <label className='font-semibold'>{each.label}</label>
                            {each.required && <p className='text-red-500 font-semibold'>*</p>}
                        </span>

                        {/* Category Input */}
                        {each.name === "category" && (<Controller
                            name={each.name}
                            control={control}
                            render={({ field }) => (
                                <SelectFieldComponent {...field} options={categoryOptions} defaultValue="initial" />
                            )}
                        />)}

                        {/* Desc input*/}
                        {each.name === "incidentDesc" && (
                            <Controller
                                name={each.name}
                                control={control}
                                render={({ field }) => (
                                    <textarea rows={3} placeholder='Start Typing here...' className='w-full h-[186px] rounded-xl p-4 border border-gray-300 outline-none text-lg resize-none' {...field} />
                                )}
                            />
                        )}

                        {/* attach file input */}
                        {each.name === "attachFile" && (
                            <span className='w-full border border-gray-300 p-4 rounded-xl'>
                                <input type='file' {...register("attachFile")} />
                            </span>
                        )}

                        {/* location input */}
                        {each.name === "location" && (
                            <Controller
                                name={each.name}
                                control={control}
                                render={({ field }) => (
                                    <input {...field} type='text' placeholder='Enter your location manually' className='w-full text-lg p-4 rounded-xl border border-gray-200 outline-none' />
                                )}
                            />
                        )}
                        {errors[each.name] && (
                            <p className='text-red-500 font-semibold text-xs'>{errors[each.name]?.message as string}hello </p>
                        )}
                    </div>
                ))}

                {/* Buttons */}
                <section className='flex flex-row items-center justify-end space-x-3 mt-4'>
                    <NeutralButton className='border border-gray-200 px-6'>
                        <p>Cancel</p>
                    </NeutralButton>

                    <ActionButton className='bg-primaryBlue-300 text-white px-6 hover:opacity-80 hover:transition-all hover:duration-200' type='submit'>
                        <div className='flex flex-row space-x-2 items-center justify-center'>
                            <p>Submit Report</p>
                            <FaArrowRight className='text-white' />
                        </div>
                    </ActionButton>
                </section>
            </form>
        </main>

    )
}

export default ReportModal
// Rape, sexual abuse, violence