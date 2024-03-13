import type { VueElement } from "vue";
import type { AppLayoutsEnum } from "@/layouts/layouts.types";

declare module 'vue-router' {
    interface RouteMeta {
        layout?: AppLayoutsEnum;
        layoutComponent?: VueElement
    }
}

export enum RouteNamesEnum {
    dashboard = 'dashboard',
    portfolio = 'portfolio',
    article = 'articles',
    company = 'markets',
    watchlist = 'watchlist',
    screener = 'screener',
}