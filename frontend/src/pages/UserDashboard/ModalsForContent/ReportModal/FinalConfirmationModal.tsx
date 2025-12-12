  import ModalComponent from '../../../../component/Modals/ModalComponent';
  import type { reportFormValidationSchemaType } from '../../../../schemas/reportFormValidation'
  import confirmIcon from "../../../../assets/padlockIcon.webp"
  import ActionButton from '../../../../component/FormButtons/ActionButton';
  import { FaArrowRight } from 'react-icons/fa';
  import { useState } from 'react';
  import ReportSentSuccessModal from './ReportSentSuccessModal';

  type FinalConfirmationModalType = {
    formData: reportFormValidationSchemaType | null
    openModal: boolean;
    onClose: () => void
    onSuccess: ()=>void
  }





  const FinalConfirmationModal = ({ formData, openModal, onClose, onSuccess }: FinalConfirmationModalType) => {
    const [checked, setChecked] = useState<boolean>(false)
    const [showSuccessModal, setShowSuccessModal] = useState<boolean>(false)

    const handleSubmitReport = () => {
      console.log(formData)
      //Pass the formData to backend.

      //Backend sends success response then frontend shows the success modal
      //Close confirmation modal
      onClose()

      //Show success Modal
      onSuccess()

      
    }

    return (
      <>
      {showSuccessModal && <ReportSentSuccessModal openModal={showSuccessModal} onClose={()=>setShowSuccessModal(false)}/>}
        <ModalComponent open={openModal} onClose={onClose} footer={[]}>
          <section className='mt-4 flex flex-col items-center justify-center '>

            <div>
              <img src={confirmIcon} alt="safemind_confirm_report" />
            </div>

            <div className='flex flex-col items-center justify-center'>
              <h1 className='text-[28px] font-semibold'>Final Confirmation</h1>
              <p className='text-[16px] text-black/50 text-center py-2' >Take a moment to verify your details. Your report will be sealed on an immutable blockchain layer, guaranteeing transparency and preventing any NGO or third party from modifying your record.</p>
            </div>

            <div className='bg-[#F2F9FF] w-full p-3 rounded-lg mt-4 flex space-x-3 items-center'>
              <input type='checkbox' name='checkbox_confirmation' onChange={(e) => e.target.checked ? setChecked(true) : setChecked(false)} />
              <label htmlFor="checkbox_confirmation">I declare that the information provided is true and accurate to the best of my knowledge.</label>
            </div>

            <div className='flex w-full justify-end mt-6'>
              <ActionButton className='bg-primaryBlue-300 text-white px-6 hover:opacity-80 hover:transition-all hover:duration-200' type='button' disabled={!checked} onClick={handleSubmitReport}>
                <div className='flex flex-row space-x-2 items-center justify-center'>
                  <p>Confirm & Submit</p>
                  <FaArrowRight className='text-white' />
                </div>
              </ActionButton>
            </div>
          </section>
        </ModalComponent>
      </>
    )
  }

  export default FinalConfirmationModal