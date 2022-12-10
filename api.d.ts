export type Optional<T> = T | undefined

export interface LosungData {
    book: Book
    verseData: VerseData
    verses: Verses
}

export interface Book {
    tanachTitle: TanachTitle
    bookTitle: BookTitle
}

export interface TanachTitle {
    english: string
    hebrew: string
}

export interface BookTitle {
    english: string
    hebrew: string
}

export interface VerseData {
    data: Data
    isMultiVerses: boolean
}

export interface Data {
    full: string
    book: string
    chapterVerse: string
    chapter: number
    verse: number
}

export interface Verses {
    hebrew: Hebrew
    german: German
}

export type VersesType = Hebrew | German;

export interface VersesLanguage {
    date: string
    sunday: string | any
    losungText: string
    losungVerse: string
}

export interface Hebrew extends VersesLanguage {
    n: string
    w: string[]
}

export interface German extends VersesLanguage {
    Datum: string
    Wtag: string
    Sonntag: string | any
    Losungstext: string
    Losungsvers: string
    Lehrtext: string
    Lehrtextvers: string
}
