// Components
import { BaseProgressLinear } from "@/apps/visagiste/components/BaseProgressLinear";

// Utilities
import {computed, h} from "vue";
import {getCurrentInstanceName, propsFactory} from "@/apps/visagiste/utils";

// Types
import type {ExtractPropTypes, SetupContext} from "vue";
import type {SlotsToProps} from "@/apps/visagiste/utils";

export interface LoaderSlotProps {
	color: string | undefined
	isActive: boolean
}

export interface LoaderProps {
	loading?: boolean | string
}

// Composables
export const useLoaderProps = propsFactory({
	loading: [Boolean, String],
}, 'loader')

export function useLoader (
	props: LoaderProps,
	name = getCurrentInstanceName(),
) {
	const loaderClasses = computed(() => ({
		[`${name}--loading`]: props.loading,
	}))

	return { loaderClasses }
}

export function LoaderSlot (
	props: {
		absolute?: boolean,
		active: boolean,
		name: string,
		color?: string,
	} & ExtractPropTypes<SlotsToProps<{
		default: LoaderSlotProps
	}>>,
	{ slots }: SetupContext,
) {
	return h(
		'div',
		{
			class: `${props.name}__loader`
		},
		{
			default: () => slots.default?.({
				color: props.color,
				isActive: props.active,
			} as LoaderSlotProps) || h(
				BaseProgressLinear,
				{
					absolute: props.absolute,
					active: props.active,
					color: props.color,
					height: "2",
					indeterminate: true,
			})
		}
	)
}
