import { test, expect } from '@playwright/test';

test('Positive Login Test', async ({ page }) => {
  await page.goto('https://practice.expandtesting.com/login');

  await page.getByLabel('Username').fill('practice');
  await page.getByLabel('Password').fill('SuperSecretPassword!');
  await page.getByRole('button', { name: 'Login' }).click();

  await expect(page).toHaveURL(/secure/);
  await expect(page.getByText('You logged into a secure area!')).toBeVisible();
});