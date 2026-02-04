import requests
from urllib.parse import urlparse

from brochurizer import Brochurizer


def normalize_url(url: str) -> str:
    """Ensure URL has a scheme. If missing, prepend https://"""
    parsed = urlparse(url)
    if not parsed.scheme:  # no http/https given
        url = "https://" + url
    return url


def is_url_valid(url: str) -> bool:
    parsed = urlparse(url)
    is_valid = all([parsed.scheme, parsed.netloc])
    if not is_valid:
        print("Invalid URL. Please enter a valid URL (e.g. example.com)")
        return False
    return True


def is_url_reachable(url: str) -> bool:
    """Check if a URL is reachable (HEAD first, then GET if necessary)."""
    try:
        # Try HEAD request first
        response = requests.head(url, timeout=3, allow_redirects=True)
        if response.status_code >= 400:
            # Some servers reject HEAD, fallback to GET
            response = requests.get(url, timeout=3, stream=True, allow_redirects=True)
        if response.status_code >= 400:
            print("Webpage in the given URL is not reachable. Retry with a different URL.")
            return False
        return True
    except requests.RequestException as e:
        print(f"Error reaching the URL: {e}. Retry with a different URL.")
        return False


def prompt_for_url():
    while True:
        url = input("Enter the URL of the page to create brochure: ").strip().lower()
        url = normalize_url(url)
        if not is_url_valid(url):
            continue
        if not is_url_reachable(url):
            continue
        print(f"Selected URL: {url}")
        return url

def prompt_for_translation():
    while True:
        supported_languages = ["spanish", "english", "french", "chinese", "german"]
        language = input(f"Enter the language to translate the brochure. (Default: None. "
                         f"Supported: {supported_languages}): ").strip().lower()
        if not language:
            print(f"Translation language was not specified. Brochure will not be translated.")
            return None
        if language not in supported_languages:
            print(f"Translation language was not supported. "
                  f"Please select a valid language from {supported_languages}.")
            continue
        print(f"Selected Language: {language}")
        return language


def prompt_for_export():
    export = input("Do you want to export the brochure as a markdown file? (Y/n): ").strip().lower() or 'y'
    return export == 'y'



def main():
    while True:
        try:
            url = prompt_for_url()
            language = prompt_for_translation()
            export = prompt_for_export()
            brochurizer = Brochurizer(url=url)
            brochurizer.create_brochure(language=language, export=export)
            break
        except (ValueError, OSError) as e:
            print(f"Brochure creation failed: {e}")
            retry = input("Do you want to retry? (Y/n): ").strip().lower() or 'y'
            if retry != 'y':
                break
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break


if __name__ == '__main__':
    main()
