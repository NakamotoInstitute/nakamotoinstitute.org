# Satoshi Nakamoto Institute

The SNI website is comprised of a headless CMS built with FastAPI and a frontend built with NextJS.

## Local Installation Instructions

### Server Setup

The server relies on Docker Compose for environment management. Ensure Docker Compose is installed on your system. To aid in local development, [`just`](https://github.com/casey/just) commands are also provided.

- **Getting Started**:

  1. Access the server directory: `cd server`.
  2. Set the `ENV` environment variable to `local` (if using `just`): `export ENV=local`.
  3. Build the Docker environment:
     - Execute: `docker compose -f docker-compose.local.yml build`
     - Or use `just build` for a simplified process.
  4. Launch the Docker environment:
     - Execute: `docker compose -f docker-compose.local.yml up -d`
     - Or use `just up` for convenience.

  This will automatically handle data migrations and imports.

- **API Access**: The API is accessible at `http://localhost:8000`.

- **Local Document Serving**: For local serving of PDFs, ePubs, etc., download the necessary files from [here](https://cdn.nakamotoinstitute.org/docs/sni-docs.zip) and place them in `server/static/docs`.

### Client Setup

The frontend uses [`pnpm`](https://github.com/pnpm/pnpm) for package management. Ensure `pnpm` is installed before proceeding.

- **Getting Started**:

  1. Navigate to the client directory: `cd client`.
  2. Update your `/etc/hosts` file with `satoshi.localhost`:
     ```
     127.0.0.1   satoshi.localhost
     ::1         satoshi.localhost
     ```
     **Note:** if you do not want these redirects, instead add `.env.local` to the client directory:
     ```
     MAP_DOMAIN=false
     ```
  3. Install dependencies: `pnpm i`.
  4. Start the development server: `pnpm dev`.

- **Website Access**: The site is available at `http://localhost:3000`.

## Internationalization and Localization (i18n and l10n)

The SNI platform is designed with i18n and l10n at its core, actively supporting and encouraging the translation of content across various sections, including the Mempool, the library, content pages, and application strings.

### Mempool Translations

To contribute Mempool translations:

- **Markdown Front Matter**: Include the required metadata using the schema below:

  ```
  title: # Translated post title
  slug: # Translated slug (ASCII only) (Optional)
  excerpt: # Key quote (refer to English posts) (Optional)
  translation_url: # Original translation URL (Optional)
  translation_site: # Original publication name (Optional)
  translation_site_url: # Original publication URL (Optional)
  translators: # List of translator slugs (Optional)
  image_alt: # Translated header image alt text (Optional)
  ```

- **File Placement**: Save the markdown file in `server/content/mempool` with the naming convention `<slug>.<ietf-code>.md` (e.g., `speculative-attack.es.md`).

### Library Translations

For library content translations, follow these guidelines:

- **Markdown Front Matter**: Utilize the schema below for metadata:

  ```
  title: # Translated document title
  slug: # Translated slug (ASCII only) (Optional)
  subtitle: # Translated subtitle (Optional)
  display_title: # Display title in the translated language (Optional)
  external: # Source URL of the translation (Optional)
  sort_title: # Title for sorting purposes (Optional)
  image_alt: # Translated document header image alt text (Optional)
  formats: # Available formats [pdf, epub, mobi, txt] (Optional)
  translators: # Translator slugs list (Optional)
  ```

- **File Placement**: Save the markdown file in `server/content/library` with the naming convention `<slug>.<ietf-code>.md` (e.g., `bitcoin.es.md`).

### Content Pages & Application Strings

- **Localized Content Pages**: Locate content pages within `client/content/pages` and add localized files using the `<filename>.<ietf-code>.md` format.
- **Application Strings Localization**: Application strings are found under `client/locales`.

### General Guidelines

- **New Languages**: To introduce a new language, update `Locales` and `LocaleType` in `server/sni/constants.py`, as well as `languages` and `locales` in `client/i18n.ts`. Then, execute `pnpm translate:extract` within the `client` directory.

---

NakamotoInstitute.org is licensed under the GNU Affero License.
