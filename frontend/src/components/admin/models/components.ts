import {AdminComponentName} from "@/types/admin.types";

interface PreviousComponentList {
    [p: string]: AdminComponentName
}

export const previousComponentList: PreviousComponentList = {
    AdminModel: AdminComponentName.MODELS,
    AdminModels: AdminComponentName.EMPTY,
    AdminDashboard: AdminComponentName.EMPTY,
    AdminStaff: AdminComponentName.EMPTY,
    AdminSettings: AdminComponentName.EMPTY,
}