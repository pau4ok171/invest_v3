import type {Component} from "vue";
import type { AppLayoutsEnum } from "@/layouts/layouts.types";

declare module 'vue-router' {
    interface RouteMeta {
        layout?: AppLayoutsEnum;
        layoutComponent?: Component
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
    page_not_found = 'page_not_found',
    admin = 'admin',
}

export enum RoutesHeaderEnum {
    dashboard = 'dashboard',
    portfolio = 'portfolio',
    article = 'articles',
    company = 'markets',
    watchlist = 'watchlist',
    screener = 'screener',
}