import { z } from "zod";

export const reportFormValidationSchema = z.object({
  category: z.enum(["rape", "sexual abuse", "violence", "others"], {
    message: "Please select a value",
  }),
  incidentDesc: z
    .string({ message: "Describe what happened!" })
    .trim()
    .min(50, { message: "Minimum of 50 characters." }),
  attachFile: z
    .any().optional()
    .refine((files) => files instanceof FileList, "File is required").optional()
    .refine((files) => files?.length > 0, "Please upload a file").optional(),
  // .refine(
  //   (files) => ["image/png", "image/jpeg"].includes(files[0].type),
  //   "Only JPG or PNG allowed"
  // ),
  location: z.string().optional()


});

export type reportFormValidationSchemaType = z.infer<typeof reportFormValidationSchema>
