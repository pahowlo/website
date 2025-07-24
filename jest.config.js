export default {
  // Use ts-jest preset for TypeScript support
  preset: "ts-jest",

  // Simulates browser environment
  testEnvironment: "jsdom",

  roots: ["<rootDir>/src"],
  testMatch: ["**/*.test.ts"],

  // How to transform files before testing (using ts-jest to compile TypeScript)
  transform: {
    "^.+\\.ts$": ["ts-jest", { useESM: true }],
  },
  extensionsToTreatAsEsm: [".ts"],
  // Coverage reports
  collectCoverageFrom: [
    "src/**/*.ts",
    "!src/**/*.d.ts",
    "!src/**/*.test.ts",
  ],
  coverageDirectory: "coverage",
  coverageReporters: ["text", "lcov", "html"],
}
