import type { VueElement } from "vue";
import type { AppLayoutsEnum } from "@/layouts/layouts.types";

declare module 'vue-router' {
    interface RouteMeta {
        layout?: AppLayoutsEnum;
        layoutComponent?: VueElement
    }
}

export enum RouteNamesEnum {
    home = 'home',
    dashboard = 'dashboard',
    portfolio = 'portfolio',
    article = 'articles',
    company_list = 'markets',
    company_detail = 'company_detail',
    watchlist = 'watchlist',
    screener = 'screener',
}

export enum RoutesHeaderEnum {
    dashboard = 'dashboard',
    portfolio = 'portfolio',
    article = 'articles',
    company = 'markets',
    watchlist = 'watchlist',
    screener = 'screener',
}