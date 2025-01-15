import { createJavascriptTransition } from "@/apps/visagiste/components/transitions/createTransition";

import ExpandTransitionGenerator from './expand-transition'


// Javascript transitions
export const BaseExpandTransition = createJavascriptTransition('expand-transition', ExpandTransitionGenerator())
export const BaseExpandXTransition = createJavascriptTransition('expand-x-transition', ExpandTransitionGenerator('', true))

export type BaseExpandTransition = InstanceType<typeof BaseExpandTransition>
export type BaseExpandXTransition = InstanceType<typeof BaseExpandXTransition>