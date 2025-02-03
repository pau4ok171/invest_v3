import { createJavascriptTransition, createCssTransition } from "./createTransition";

import ExpandTransitionGenerator from './expand-transition'

// Generic transitions
export const BaseSlideYTransition = createCssTransition('slide-y-transition')
export const BaseFadeTransition = createCssTransition('fade-transition')

// Javascript transitions
export const BaseExpandTransition = createJavascriptTransition('expand-transition', ExpandTransitionGenerator())
export const BaseExpandXTransition = createJavascriptTransition('expand-x-transition', ExpandTransitionGenerator('', true))

export type BaseExpandTransition = InstanceType<typeof BaseExpandTransition>
export type BaseExpandXTransition = InstanceType<typeof BaseExpandXTransition>
export type BaseSlideYTransition = InstanceType<typeof BaseSlideYTransition>
export type BaseFadeTransition = InstanceType<typeof BaseFadeTransition>