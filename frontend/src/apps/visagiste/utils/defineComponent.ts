import type {VNode, VNodeChild} from "vue";

export type SlotsToProps<
	U extends RawSlots,
	T = MakeInternalSlots<U>
> = {
	$children?: (
		| VNodeChild
		| (T extends { default: infer V } ? V : {})
		| { [K in keyof T]?: T[K] }
	)
	'v-slots'?: { [ K in keyof T]?: T[K] | false }
} & {
	[K in keyof T as `v-slot:${K & string}`]?: T[K] | false
}

type RawSlots = Record<string, unknown>
type Slot<T> = [T] extends [never] ? () => VNodeChild : (arg: T) => VNodeChild
type VueSlot<T> = [T] extends [never] ? () => VNode[] : (arg: T) => VNode[]
type MakeInternalSlots<T extends RawSlots> = {
	[K in keyof T]: Slot<T[K]>
}
type MakeSlots<T extends RawSlots> = {
	[K in keyof T]: VueSlot<T[K]>
}