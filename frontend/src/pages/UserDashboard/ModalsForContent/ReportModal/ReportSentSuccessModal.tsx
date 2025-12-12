import ModalComponent from "../../../../component/Modals/ModalComponent"


const ReportSentSuccessModal = ({openModal, onClose} : {openModal:boolean, onClose: ()=>void}) => {
  return (
    <ModalComponent open={openModal} onClose={onClose} footer={[]}>
        <h1>success</h1>
    </ModalComponent>
  )
}

export default ReportSentSuccessModal