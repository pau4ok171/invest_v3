// Utilities
import { getCurrentInstance } from "@/apps/visagiste/utils";

export function useScopeId () {
  const vm = getCurrentInstance('useScopeId')

  const scopeId = vm!.vnode.scopeId

  return { scopeId: scopeId ? { [scopeId]: '' } : undefined }
}