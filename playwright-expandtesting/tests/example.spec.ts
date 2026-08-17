import { test, expect } from '@playwright/test';

test('Smoke Test - Homepage loads successfully', async ({ page }) => {
  await page.goto('https://practice.expandtesting.com');

  await expect(page).toHaveTitle(/Practice/);

  await expect(
    page.getByRole('heading', { name: 'Test Automation Practice' })
  ).toBeVisible();
});