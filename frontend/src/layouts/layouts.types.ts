export enum AppLayoutsEnum {
    default = 'default',
    login = 'login',
    error = 'error',
}

export const AppLayoutToFileMap: Record<AppLayoutsEnum, string> = {
    default: 'AppLayoutDefault.vue',
    login: 'AppLayoutDefault.vue',
    error: 'AppLayoutDefault.vue',
};