export enum AppLayoutsEnum {
    default = 'default',
    admin = 'admin',
}

export const AppLayoutToFileMap: Record<AppLayoutsEnum, string> = {
    default: 'AppLayoutDefault.vue',
    admin: 'AppLayoutAdmin.vue',
};