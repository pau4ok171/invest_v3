export enum AppLayoutsEnum {
    default = 'default',
    admin = 'admin',
    empty = 'empty',
}

export const AppLayoutToFileMap: Record<AppLayoutsEnum, string> = {
    default: 'AppLayoutDefault.vue',
    admin: 'AppLayoutAdmin.vue',
    empty: 'AppLayoutEmpty.vue',
};