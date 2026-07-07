import { describe, expect, it } from "vitest";
import { ApiError } from "@/api/client";
import { formatApiError, translateApiError } from "@/composables/useApiErrorMessage";

function ruTranslator(key: string, params?: Record<string, string>): string {
  switch (key) {
    case "errors.fileNotFound":
      return "Файл не найден";
    case "errors.storedFileNotFound":
      return "Сохранённый файл не найден";
    case "errors.filenameRequired":
      return "Имя файла обязательно";
    case "errors.fileEmpty":
      return "Файл пустой";
    case "errors.fileTooLarge":
      return `Размер файла превышает ${params?.limit ?? ""} байт`;
    default:
      return key;
  }
}

describe("translateApiError", () => {
  const t = ruTranslator;

  it.each([
    { message: "File not found", expected: "Файл не найден" },
    { message: "Stored file not found", expected: "Сохранённый файл не найден" },
    { message: "Filename is required", expected: "Имя файла обязательно" },
    { message: "File is empty", expected: "Файл пустой" },
    {
      message: "file exceeds maximum upload size of 52428800 bytes",
      expected: "Размер файла превышает 52428800 байт",
    },
  ])("translates: $message", ({ message, expected }) => {
    expect(translateApiError(message, t)).toBe(expected);
  });

  it("returns unknown message unchanged", () => {
    expect(translateApiError("Something went wrong", t)).toBe("Something went wrong");
  });
});

describe("formatApiError", () => {
  it("returns fallback for non-API errors", () => {
    expect(formatApiError(new Error("x"), "fallback", "ru", ruTranslator)).toBe("fallback");
  });

  it("returns english message on en locale", () => {
    const error = new ApiError(404, "File not found");
    expect(formatApiError(error, "fallback", "en", ruTranslator)).toBe("File not found");
  });

  it("translates message on ru locale", () => {
    const error = new ApiError(404, "File not found");
    expect(formatApiError(error, "fallback", "ru", ruTranslator)).toBe("Файл не найден");
  });
});
