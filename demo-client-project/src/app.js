// Sample application with i18n usage
import i18n from 'i18n';

function showWelcomeMessage() {
  // Using internationalization keys
  const title = i18n.t('welcome.title');
  const message = i18n.t('welcome.message');
  
  document.getElementById('welcome-title').textContent = title;
  document.getElementById('welcome-message').textContent = message;
}

function displayUserInfo(user) {
  // More i18n key usage
  const nameLabel = i18n.t('user.name');
  const emailLabel = i18n.t('user.email');
  
  console.log(`${nameLabel}: ${user.name}`);
  console.log(`${emailLabel}: ${user.email}`);
}

// This key is missing in the translation files
function showErrorMessage() {
  alert(i18n.t('errors.unexpected'));
}

export { showWelcomeMessage, displayUserInfo, showErrorMessage }; 