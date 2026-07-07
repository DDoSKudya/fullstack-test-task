import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";
import { deleteFile, fetchAlerts, fetchFiles, uploadFile } from "@/api/client";

const POLL_MS = 1000;

export function useFilesQuery() {
  return useQuery({
    queryKey: ["files"],
    queryFn: fetchFiles,
    refetchInterval: POLL_MS,
  });
}

export function useAlertsQuery() {
  return useQuery({
    queryKey: ["alerts"],
    queryFn: fetchAlerts,
    refetchInterval: POLL_MS,
  });
}

export function useUploadMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ title, file }: { title: string; file: File }) => uploadFile(title, file),
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["files"] }),
        queryClient.invalidateQueries({ queryKey: ["alerts"] }),
      ]);
    },
  });
}

export function useDeleteMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (fileId: string) => deleteFile(fileId),
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["files"] }),
        queryClient.invalidateQueries({ queryKey: ["alerts"] }),
      ]);
    },
  });
}
