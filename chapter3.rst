.. image:: biopython.jpg

.. Overview

.. index::
   single: Chapter 3  Sequence objects;Chapter 3  Sequence objects

Chapter 3  シーケンスオブジェクト
=================================

.. Biological sequences are arguably the central object in Bioinformatics, and in this chapter we’ll introduce the Biopython mechanism for dealing with sequences, the Seq object.Chapter 4 will introduce the related SeqRecord object, which combines the sequence information with any annotation, used again in Chapter 5 for Sequence Input/Output.

Biological sequences are arguably the central object in Bioinformatics, and in this chapter we’ll introduce the Biopython mechanism for dealing with sequences, the Seq object.Chapter 4 will introduce the related SeqRecord object, which combines the sequence information with any annotation, used again in Chapter 5 for Sequence Input/Output.

.. Sequences are essentially strings of letters like AGTACACTGGT, which seems very natural since this is the most common way that sequences are seen in biological file formats.

Sequences are essentially strings of letters like AGTACACTGGT, which seems very natural since this is the most common way that sequences are seen in biological file formats.

.. There are two important differences between Seq objects and standard Python strings.First of all, they have different methods. Although the Seq object supports many of the same methods as a plain string, its translate() method differs by doing biological translation, and there are also additional biologically relevant methods like reverse_complement().Secondly, the Seq object has an important attribute, alphabet, which is an object describing what the individual characters making up the sequence string “mean”, and how they should be interpreted. For example, is AGTACACTGGT a DNA sequence, or just a protein sequence that happens to be rich in Alanines, Glycines, Cysteinesand Threonines?

There are two important differences between Seq objects and standard Python strings.First of all, they have different methods. Although the Seq object supports many of the same methods as a plain string, its translate() method differs by doing biological translation, and there are also additional biologically relevant methods like reverse_complement().Secondly, the Seq object has an important attribute, alphabet, which is an object describing what the individual characters making up the sequence string “mean”, and how they should be interpreted. For example, is AGTACACTGGT a DNA sequence, or just a protein sequence that happens to be rich in Alanines, Glycines, Cysteinesand Threonines?

.. index::
   pair: 3.1  Sequences and Alphabets;3.1  Sequences and Alphabets

3.1  Sequences and Alphabets
----------------------------

.. The alphabet object is perhaps the important thing that makes the Seq object more than just a string. The currently available alphabets for Biopython are defined in the Bio.Alphabet module. We’ll use the IUPAC alphabets (http://www.chem.qmw.ac.uk/iupac/) here to deal with some of our favorite objects: DNA, RNA and Proteins.

The alphabet object is perhaps the important thing that makes the Seq object more than just a string. The currently available alphabets for Biopython are defined in the Bio.Alphabet module. We’ll use the IUPAC alphabets (http://www.chem.qmw.ac.uk/iupac/) here to deal with some of our favorite objects: DNA, RNA and Proteins.

.. Bio.Alphabet.IUPAC provides basic definitions for proteins, DNA and RNA, but additionally provides the ability to extend and customize the basic definitions. For instance, for proteins, there is a basic IUPACProtein class, but there is an additional ExtendedIUPACProtein class providing for the additional elements “U” (or “Sec” for selenocysteine) and “O” (or “Pyl” for pyrrolysine), plus the ambiguous symbols “B” (or “Asx” for asparagine or aspartic acid), “Z” (or “Glx” for glutamine or glutamic acid), “J” (or “Xle” for leucine isoleucine) and “X” (or “Xxx” for an unknown amino acid). For DNA you’ve got choices of IUPACUnambiguousDNA, which provides for just the basic letters, IUPACAmbiguousDNA (which provides for ambiguity letters for every possible situation) and ExtendedIUPACDNA, which allows letters for modified bases. Similarly, RNA can be represented by IUPACAmbiguousRNA or IUPACUnambiguousRNA.

Bio.Alphabet.IUPAC provides basic definitions for proteins, DNA and RNA, but additionally provides the ability to extend and customize the basic definitions. For instance, for proteins, there is a basic IUPACProtein class, but there is an additional ExtendedIUPACProtein class providing for the additional elements “U” (or “Sec” for selenocysteine) and “O” (or “Pyl” for pyrrolysine), plus the ambiguous symbols “B” (or “Asx” for asparagine or aspartic acid), “Z” (or “Glx” for glutamine or glutamic acid), “J” (or “Xle” for leucine isoleucine) and “X” (or “Xxx” for an unknown amino acid). For DNA you’ve got choices of IUPACUnambiguousDNA, which provides for just the basic letters, IUPACAmbiguousDNA (which provides for ambiguity letters for every possible situation) and ExtendedIUPACDNA, which allows letters for modified bases. Similarly, RNA can be represented by IUPACAmbiguousRNA or IUPACUnambiguousRNA.

.. The advantages of having an alphabet class are two fold. First, this gives an idea of the type of information the Seq object contains. Secondly, this provides a means of constraining the information, as a means of type checking.

The advantages of having an alphabet class are two fold. First, this gives an idea of the type of information the Seq object contains. Secondly, this provides a means of constraining the information, as a means of type checking.

.. Now that we know what we are dealing with, let’s look at how to utilize this class to do interesting work.You can create an ambiguous sequence with the default generic alphabet like this:

Now that we know what we are dealing with, let’s look at how to utilize this class to do interesting work.You can create an ambiguous sequence with the default generic alphabet like this:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> my_seq = Seq("AGTACACTGGT")
    >>> my_seq
    Seq('AGTACACTGGT', Alphabet())
    >>> my_seq.alphabet
    Alphabet()


.. However, where possible you should specify the alphabet explicitly when creating your sequence objects - in this case an unambiguous DNA alphabet object:

However, where possible you should specify the alphabet explicitly when creating your sequence objects - in this case an unambiguous DNA alphabet object:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import IUPAC
    >>> my_seq = Seq("AGTACACTGGT", IUPAC.unambiguous_dna)
    >>> my_seq
    Seq('AGTACACTGGT', IUPACUnambiguousDNA())
    >>> my_seq.alphabet
    IUPACUnambiguousDNA()


.. Unless of course, this really is an amino acid sequence:

Unless of course, this really is an amino acid sequence:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import IUPAC
    >>> my_prot = Seq("AGTACACTGGT", IUPAC.protein)
    >>> my_prot
    Seq('AGTACACTGGT', IUPACProtein())
    >>> my_prot.alphabet
    IUPACProtein()


.. index::
   pair: 3.2  Sequences act like strings;3.2  Sequences act like strings

3.2  Sequences act like strings
-------------------------------

.. In many ways, we can deal with Seq objects as if they were normal Python strings, for example getting the length, or iterating over the elements:

いろいろな意味で、Seqオブジェクトを通常のPython stringのように扱うことができます。例えば、長さを取得したり要素をイテレートできます。:

.. code-block:: python

    from Bio.Seq import Seq
    from Bio.Alphabet import IUPAC
    my_seq = Seq("GATCGATGGGCCTATATAGGATCGAAAATCGC", IUPAC.unambiguous_dna)
    for index, letter in enumerate(my_seq):
        print index, letter
    print len(letter)


.. You can access elements of the sequence in the same way as for strings (but remember, Python counts from zero!):

文字列に対して行うのと同じ方法で、シーケンスの要素にアクセスすることができます(ただしPythonは0からカウントすることを覚えておいてください!):

.. code-block:: python

    >>> print my_seq[0] #first letter
    >>> print my_seq[2] #third letter
    >>> print my_seq[-1] #last letter


.. The Seq object has a .count() method, just like a string.Note that this means that like a Python string, this gives anon-overlapping count:

Seqオブジェクトには、stringのように .count() メソッドがあります。Python のstringのように、重複したカウントを得ることができます:

.. code-block:: python

    >>> "AAAA".count("AA")
    2
    >>> Seq("AAAA").count("AA")
    2


.. For some biological uses, you may actually want an overlapping count(i.e. 3 in this trivial example). When searching for single letters, thismakes no difference:

生物学的用法で、重複カウント(3つの簡単なサンプル)を得ることができます。1文字の時は、違いがありません:

.. code-block:: python

    >>> len(my_seq)
    32
    >>> my_seq.count("G")
    10
    >>> 100 * float(my_seq.count("G") + my_seq.count("C")) / len(my_seq)
    46.875


.. While you could use the above snippet of code to calculate a GC%, note that the Bio.SeqUtils module has several GC functions already built. For example:

上のコードで、GC%を計算することができましたが、Bio.SeqUtilsモジュールには、GCの関数がいくつか存在しています。例えば:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import IUPAC
    >>> from Bio.SeqUtils import GC
    >>> my_seq = Seq('GATCGATGGGCCTATATAGGATCGAAAATCGC', IUPAC.unambiguous_dna)
    >>> GC(my_seq)
    46.875


.. Note that using the Bio.SeqUtils.GC() function should automatically cope with mixed case sequences and the ambiguous nucleotide S which means G or C.

SeqUtils.GC() を使うと自動的に、大文字小文字の混ざったシーケンスや、GまたはCを表すヌクレオチドSを扱うことができます。

.. Also note that just like a normal Python string, the Seq object is in some ways “read-only”. If you need to edit your sequence, for example simulating a point mutation, look at the Section 3.12 below which talks about the MutableSeq object.

Also note that just like a normal Python string, the Seq object is in some ways “read-only”. If you need to edit your sequence, for example simulating a point mutation, look at the Section 3.12 below which talks about the MutableSeq object.

.. index::
   pair: 3.3  Slicing a sequence;3.3  Slicing a sequence

3.3  シーケンスのスライス
-------------------------

.. A more complicated example, let’s get a slice of the sequence:

より複雑なサンプルです、シーケンスをスライスしてみましょう:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import IUPAC
    >>> my_seq = Seq("GATCGATGGGCCTATATAGGATCGAAAATCGC", IUPAC.unambiguous_dna)
    >>> my_seq[4:12]
    Seq('GATGGGCC', IUPACUnambiguousDNA())


.. Two things are interesting to note. First, this follows the normal conventions for Python strings. So the first element of the sequence is 0 (which is normal for computer science, but not so normal for biology). When you do a slice the first item is included (i.e. 4 in this case) and the last is excluded (12 in this case), which is the way things work in Python, but of course not necessarily the way everyone in the world would expect. The main goal is to stay consistent with what Python does.

Two things are interesting to note. First, this follows the normal conventions for Python strings. So the first element of the sequence is 0 (which is normal for computer science, but not so normal for biology). When you do a slice the first item is included (i.e. 4 in this case) and the last is excluded (12 in this case), which is the way things work in Python, but of course not necessarily the way everyone in the world would expect. The main goal is to stay consistent with what Python does.

.. The second thing to notice is that the slice is performed on the sequence data string, but the new object produced is another Seq object which retains the alphabet information from the original Seq object.

２番目に、シーケンスデータ文字列に対して行われたsliceの結果得られた新しいオブジェクトは、元のSeqオブジェクトからのアルファベットの情報を持った別のSeqオブジェクトです。

.. Also like a Python string, you can do slices with a start, stop and stride (the step size, which defaults to one). For example, we can get the first, second and third codon positions of this DNA sequence:

Python stringのように、 start, stop , stride (ステップサイズで、デフォルトは1です) を使ってスライスすることができます。例として、このDNAシーケンスの、1つめ、2つめ、3つめのコドン位置を指定して取得してみましょう:

.. code-block:: python

    >>> my_seq[0::3]
    Seq('GCTGTAGTAAG', IUPACUnambiguousDNA())
    >>> my_seq[1::3]
    Seq('AGGCATGCATC', IUPACUnambiguousDNA())
    >>> my_seq[2::3]
    Seq('TAGCTAAGAC', IUPACUnambiguousDNA())


.. Another stride trick you might have seen with a Python string is the use of a -1 stride to reverse the string. You can do this with a Seq object too:

別の stride の使い方として、Python string で、 -1 を指定することで逆向きの文字列を取得することができます。これをSeqオブジェクトでも使うことができます:

.. code-block:: python

    >>> my_seq[::-1]
    Seq('CGCTAAAAGCTAGGATATATCCGGGTAGCTAG', IUPACUnambiguousDNA())


.. index::
   pair: 3.4  Turning Seq objects into strings;3.4  Turning Seq objects into strings

3.4  Seqオブジェクトを文字列に変換する
--------------------------------------

.. If you really do just need a plain string, for example to write to a file, or insert into a database, then this is very easy to get:

データベースに追加したり、ファイルに書き込みたいときなど、普通のstringが必要ならば、次のようにして簡単に変換することができます:

.. code-block:: python

    >>> str(my_seq)
    'GATCGATGGGCCTATATAGGATCGAAAATCGC'


.. Since calling str() on a Seq object returns the full sequence as a string,you often don’t actually have to do this conversion explicitly.Python does this automatically with a print statement:

str()にSeqオブジェクトを渡すと、シーケンス全体の普通のstringが返ります。しかし明示的に呼ぶ必要がないときもあります。Pythonは、print分で、自動的にこれを行ってくれます:

.. code-block:: python

    >>> print my_seq
    GATCGATGGGCCTATATAGGATCGAAAATCGC


.. You can also use the Seq object directly with a %s placeholder when using the Python string formatting or interpolation operator (%):

またSeqオブジェクトを、%s プレースホルダーや、補完演算子(%)に渡すことができます:

.. code-block:: python

    >>> fasta_format_string = ">Name\n%s\n" % my_seq
    >>> print fasta_format_string
    >Name
    GATCGATGGGCCTATATAGGATCGAAAATCGC


.. This line of code constructs a simple FASTA format record (without worrying about line wrapping).Section 4.5 describes a neat way to get a FASTA formattedstring from a SeqRecord object, while the more general topic of reading andwriting FASTA format sequence files is covered in Chapter 5.

この1行で、単純なFASTA形式のレコードを作ることができます(行の折り返しを気にする必要はありません)。Section 4.5 で、SeqRecordオブジェクトからFASTA形式の文字列を得るきちんとした方法を述べます。またより一般的なFASTA形式の読み書きについては、 Chapter 5でカバーします

.. NOTE: If you are using Biopython 1.44 or older, using str(my_seq)will give just a truncated representation. Instead use my_seq.tostring()(which is still available in the current Biopython releases for backwards compatibility):

NOTE: Biopython 1.44 か、それ以前のバージョンをお使いの場合、 str(my_seq) 切り捨てられたものが返ってきます。代わりに my_seq.tostring() を使ってください。(これは後方互換性を確保するために、現在のバージョンのBiopythonでも使うことができます):

.. code-block:: python

    >>> my_seq.tostring()
    'GATCGATGGGCCTATATAGGATCGAAAATCGC'


.. index::
   pair: 3.5  Concatenating or adding sequences;3.5  Concatenating or adding sequences

3.5  シーケンスの連結、追加
--------------------------------------

.. Naturally, you can in principle add any two Seq objects together - just like you can with Python strings to concatenate them. However, you can’t add sequences with incompatible alphabets, such as a protein sequence and a DNA sequence:

もちろん、Python string で文字列を連結できるように、原則として2つのSeqオブジェクトを足すことができます。しかし、たんぱく質シーケンスとDNAシーケンスのように、互換性のないアルファベットのシーケンスをつなげることはできません:

.. code-block:: python

    >>> protein_seq + dna_seq
    Traceback (most recent call last):
    ...
    TypeError: ('incompatable alphabets', 'IUPACProtein()', 'IUPACUnambiguousDNA()')


.. If you really wanted to do this, you’d have to first give both sequences generic alphabets:

本当にこれをしたいなら、まず両方のシーケンスを一般的なアルファベットのシーケンスにする必要があります:

.. code-block:: python

    >>> from Bio.Alphabet import generic_alphabet
    >>> protein_seq.alphabet = generic_alphabet
    >>> dna_seq.alphabet = generic_alphabet
    >>> protein_seq + dna_seq
    Seq('EVRNAKACGT', Alphabet())


.. Here is an example of adding a generic nucleotide sequence to an unambiguous IUPAC DNA sequence, resulting in an ambiguous nucleotide sequence:

ここでは例として、unambiguous IUPAC DNAシーケンスに、一般的なヌクレオチドシーケンスをつなげます。結果として、1つのunambiguous IUPAC DNAシーケンスが得られます:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import generic_nucleotide
    >>> from Bio.Alphabet import IUPAC
    >>> nuc_seq = Seq("GATCGATGC", generic_nucleotide)
    >>> dna_seq = Seq("ACGT", IUPAC.unambiguous_dna)
    >>> nuc_seq
    Seq('GATCGATGC', NucleotideAlphabet())
    >>> dna_seq
    Seq('ACGT', IUPACUnambiguousDNA())
    >>> nuc_seq + dna_seq
    Seq('GATCGATGCACGT', NucleotideAlphabet())


.. index::
   pair: 3.6  Changing case;3.6  Changing case

3.6  大文字小文字変換
---------------------

.. Python strings have very useful upper and lower methods for changing the case.As of Biopython 1.53, the Seq object gained similar methods which are alphabet aware.For example,

Python の文字列操作は、大文字小文字変換が非常に便利です。Biopython 1.53の、 Seq オブジェクトにも似たようなメソッドあります。例えば,

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import generic_dna
    >>> dna_seq = Seq("acgtACGT", generic_dna)
    >>> dna_seq
    Seq('acgtACGT', DNAAlphabet())
    >>> dna_seq.upper()
    Seq('ACGTACGT', DNAAlphabet())
    >>> dna_seq.lower()
    Seq('acgtacgt', DNAAlphabet())


.. These are useful for doing case insensitive matching:

大文字小文字を無視したマッチングをするのに便利です。

.. code-block:: python

    >>> "GTAC" in dna_seq
    False
    >>> "GTAC" in dna_seq.upper()
    True


.. Note that strictly speaking the IUPAC alphabets are for upper casesequences only, thus:

厳密にいえば、IUPACアルファベットは、大文字のみです。例えば:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import IUPAC
    >>> dna_seq = Seq("ACGT", IUPAC.unambiguous_dna)
    >>> dna_seq
    Seq('ACGT', IUPACUnambiguousDNA())
    >>> dna_seq.lower()
    Seq('acgt', DNAAlphabet())


.. index::
   pair: 3.7  Nucleotide sequences and (reverse) complements;3.7  Nucleotide sequences and (reverse) complements

3.7  Nucleotide sequences and (reverse) complements
---------------------------------------------------

.. For nucleotide sequences, you can easily obtain the complement or reversecomplement of a Seq object using its built-in methods:

ヌクレオチドシーケンスについて、Seqオブジェクトのビルトインメソッドを使うことでcomplement, reversecomplementを簡単に得ることができます:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import IUPAC
    >>> my_seq = Seq("GATCGATGGGCCTATATAGGATCGAAAATCGC", IUPAC.unambiguous_dna)
    >>> my_seq
    Seq('GATCGATGGGCCTATATAGGATCGAAAATCGC', IUPACUnambiguousDNA())
    >>> my_seq.complement()
    Seq('CTAGCTACCCGGATATATCCTAGCTTTTAGCG', IUPACUnambiguousDNA())
    >>> my_seq.reverse_complement()
    Seq('GCGATTTTCGATCCTATATAGGCCCATCGATC', IUPACUnambiguousDNA())


.. As mentioned earlier, an easy way to just reverse a Seq object (or aPython string) is slice it with -1 step:

以前述べたように、Seqオブジェクト(またはPythonのstring)のreverseを簡単に求める方法は、それ地震の-1ステップのsliceです:

.. code-block:: python

    >>> my_seq[::-1]
    Seq('CGCTAAAAGCTAGGATATATCCGGGTAGCTAG', IUPACUnambiguousDNA())


.. In all of these operations, the alphabet property is maintained. This is veryuseful in case you accidentally end up trying to do something weird like take the (reverse)complement of a protein sequence:

これらすべての操作を行っても、アルファベットのプロパティは保持され続けます。これはたんぱく質シーケンスの(reverse)complement を誤って取得しようとした場合に有用です:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import IUPAC
    >>> protein_seq = Seq("EVRNAK", IUPAC.protein)
    >>> protein_seq.complement()
    ...
    ValueError: Proteins do not have complements!


.. The example in Section 5.5.3 combines the Seqobject’s reverse complement method with Bio.SeqIO for sequence input/ouput.

Section 5.5.3 では、Seqオブジェクトのreverse complementの組み合わせをシーケンスの入出力を行う Bio.SeqIO を使って説明します

.. index::
   pair: 3.8  Transcription;3.8  Transcription

3.8  転写
------------------

.. Before talking about transcription, I want to try and clarify the strand issue.Consider the following (made up) stretch of double stranded DNA which encodes a short peptide:

転写について話す前に、strand問題を明確にしたいと思います。次(の構成)の短いペプチドをエンコードした二本鎖DNAを考えてください:

..   DNA coding strand (aka Crick strand, strand +1) 5’ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG3’ ||||||||||||||||||||||||||||||||||||||| 3’TACCGGTAACATTACCCGGCGACTTTCCCACGGGCTATC5’ DNA template strand (aka Watson strand, strand 1)   |  Transcription    5’AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGAUAG3’ Single stranded messenger RNA  The actual biological transcription process works from the template strand, doing a reverse complement (TCAG  CUGA) to give the mRNA. However, in Biopython and bioinformatics in general, we typically work directly with the coding strand because this means we can get the mRNA sequence just by switching T  U.

.. code-block:: python

  DNA coding strand (aka Crick strand, strand +1)
 5’ ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG 3’
    |||||||||||||||||||||||||||||||||||||||
 3’ TACCGGTAACATTACCCGGCGACTTTCCCACGGGCTATC 5’
   DNA template strand (aka Watson strand, strand 1)
                           |
                      Transcription
 5’ AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGAUAG 3’
       Single stranded messenger RNA

.. The actual biological transcription process works from the template strand, doing a reverse complement (TCAG  CUGA) to give the mRNA. However, in Biopython and bioinformatics in general, we typically work directly with the coding strand because this means we can get the mRNA sequence just by switching T  U.

The actual biological transcription process works from the template strand, doing a reverse complement (TCAG  CUGA) to give the mRNA. However, in Biopython and bioinformatics in general, we typically work directly with the coding strand because this means we can get the mRNA sequence just by switching T  U.

.. Now let’s actually get down to doing a transcription in Biopython. First, let’s create Seq objects for the coding and template DNA strands:

では実際に Biopython で転写を実行してみましょう。まずはじめに、テンプレートDNA strandとなるSeqオブジェクトを作ります:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import IUPAC
    >>> coding_dna = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG", IUPAC.unambiguous_dna)
    >>> coding_dna
    Seq('ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG', IUPACUnambiguousDNA())
    >>> template_dna = coding_dna.reverse_complement()
    >>> template_dna
    Seq('CTATCGGGCACCCTTTCAGCGGCCCATTACAATGGCCAT', IUPACUnambiguousDNA())


.. These should match the figure above - remember by convention nucleotide sequences are normally read from the 5’ to 3’ direction, while in the figure the template strand is shown reversed.

These should match the figure above - remember by convention nucleotide sequences are normally read from the 5’ to 3’ direction, while in the figure the template strand is shown reversed.

.. Now let’s transcribe the coding strand into the corresponding mRNA, using the Seq object’s built in transcribe method:

では、Seqオブジェクトに組み込まれている transcribe() メソッドを使って、coding strand を対応する mRNAに転写してみましょう:

.. code-block:: python

    >>> coding_dna
    Seq('ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG', IUPACUnambiguousDNA())
    >>> messenger_rna = coding_dna.transcribe()
    >>> messenger_rna
    Seq('AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGAUAG', IUPACUnambiguousRNA())


.. As you can see, all this does is switch T  U, and adjust the alphabet.

見て分かるように、やっていることはTをUに変えて、アルファベットを補正しました

.. If you do want to do a true biological transcription starting with the template strand, then this becomes a two-step process:

もしtemplate strandからはじめて生物学の本来の転写を行いたいなら、２段階のプロセスになります:

.. code-block:: python

    >>> template_dna.reverse_complement().transcribe()
    Seq('AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGAUAG', IUPACUnambiguousRNA())


.. The Seq object also includes a back-transcription method for going from the mRNA to the coding strand of the DNA. Again, this is a simple U  T substitution and associated change of alphabet:

The Seq object also includes a back-transcription method for going from the mRNA to the coding strand of the DNA. Again, this is a simple U  T substitution and associated change of alphabet:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import IUPAC
    >>> messenger_rna = Seq("AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGAUAG", IUPAC.unambiguous_rna)
    >>> messenger_rna
    Seq('AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGAUAG', IUPACUnambiguousRNA())
    >>> messenger_rna.back_transcribe()
    Seq('ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG', IUPACUnambiguousDNA())


.. Note: The Seq object’s transcribe and back_transcribe methodswere added in Biopython 1.49. For older releases you would have to use the Bio.Seqmodule’s functions instead, see Section 3.14.

Note: The Seq object’s transcribe and back_transcribe methodswere added in Biopython 1.49. For older releases you would have to use the Bio.Seqmodule’s functions instead, see Section 3.14.

.. index::
   pair: 3.9  Translation;3.9  Translation

3.9  翻訳
----------------

.. Sticking with the same example discussed in the transcription section above,now let’s translate this mRNA into the corresponding protein sequence - again takingadvantage of one of the Seq object’s biological methods:

Sticking with the same example discussed in the transcription section above,now let’s translate this mRNA into the corresponding protein sequence - again takingadvantage of one of the Seq object’s biological methods:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import IUPAC
    >>> messenger_rna = Seq("AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGAUAG", IUPAC.unambiguous_rna)
    >>> messenger_rna
    Seq('AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGAUAG', IUPACUnambiguousRNA())
    >>> messenger_rna.translate()
    Seq('MAIVMGR*KGAR*', HasStopCodon(IUPACProtein(), '*'))


.. You can also translate directly from the coding strand DNA sequence:

また、coding strand DNA strandから直接翻訳することもできます:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import IUPAC
    >>> coding_dna = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG", IUPAC.unambiguous_dna)
    >>> coding_dna
    Seq('ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG', IUPACUnambiguousDNA())
    >>> coding_dna.translate()
    Seq('MAIVMGR*KGAR*', HasStopCodon(IUPACProtein(), '*'))


.. You should notice in the above protein sequences that in addition to the end stop character, there is an internal stop as well. This was a deliberate choice of example, as it gives an excuse to talk about some optional arguments, including different translation tables (Genetic Codes).

You should notice in the above protein sequences that in addition to the end stop character, there is an internal stop as well. This was a deliberate choice of example, as it gives an excuse to talk about some optional arguments, including different translation tables (Genetic Codes).

.. The translation tables available in Biopython are based on those from the NCBI (see the next section of this tutorial). By default, translation will use the standard genetic code (NCBI table id 1).Suppose we are dealing with a mitochondrial sequence. We need to tell the translation function to use the relevant genetic code instead:

Biopythonでは、NCBI (このチュートリアルの次のセクションで扱います) の翻訳テーブルを利用することができます。デフォルトでは、翻訳において、標準遺伝コード(NCBIテーブルid 1)を使います。もしミトコンドリアのシーケンスを扱おうとするならば、代わりに関連した遺伝コードを使うことをtranslation関数に伝える必要があります:

.. code-block:: python

    >>> coding_dna.translate(table="Vertebrate Mitochondrial")
    Seq('MAIVMGRWKGAR*', HasStopCodon(IUPACProtein(), '*'))


.. You can also specify the table using the NCBI table number which is shorter, and often included in the feature annotation of GenBank files:

また、簡単にNCBIのテーブル番号を使ってテーブルを指定することもできます。これはより短く、GenBankファイルのfeature annoationを含んでいることがしばしばあります:

.. code-block:: python

    >>> coding_dna.translate(table=2)
    Seq('MAIVMGRWKGAR*', HasStopCodon(IUPACProtein(), '*'))


.. Now, you may want to translate the nucleotides up to the first in frame stop codon,and then stop (as happens in nature):

Now, you may want to translate the nucleotides up to the first in frame stop codon,and then stop (as happens in nature):

.. code-block:: python

    >>> coding_dna.translate()
    Seq('MAIVMGR*KGAR*', HasStopCodon(IUPACProtein(), '*'))
    >>> coding_dna.translate(to_stop=True)
    Seq('MAIVMGR', IUPACProtein())
    >>> coding_dna.translate(table=2)
    Seq('MAIVMGRWKGAR*', HasStopCodon(IUPACProtein(), '*'))
    >>> coding_dna.translate(table=2, to_stop=True)
    Seq('MAIVMGRWKGAR', IUPACProtein())


.. Notice that when you use the to_stop argument, the stop codon itselfis not translated - and the stop symbol is not included at the end of your proteinsequence.

Notice that when you use the to_stop argument, the stop codon itselfis not translated - and the stop symbol is not included at the end of your proteinsequence.

.. You can even specify the stop symbol if you don’t like the default asterisk:

デフォルトのアスタリスクが嫌ならば、stop symbolを指定することもできます:

.. code-block:: python

    >>> coding_dna.translate(table=2, stop_symbol="@")
    Seq('MAIVMGRWKGAR@', HasStopCodon(IUPACProtein(), '@'))


.. Now, suppose you have a complete coding sequence CDS, which is to say anucleotide sequence (e.g. mRNA  after any splicing) which is a whole numberof codons (i.e. the length is a multiple of three), commences with a startcodon, ends with a stop codon, and has no internal in-frame stop codons.In general, given a complete CDS, the default translate method will do whatyou want (perhaps with the to_stop option). However, what if yoursequence uses a non-standard start codon? This happens a lot in bacteria for example the gene yaaX in E. coli K12:

Now, suppose you have a complete coding sequence CDS, which is to say anucleotide sequence (e.g. mRNA  after any splicing) which is a whole numberof codons (i.e. the length is a multiple of three), commences with a startcodon, ends with a stop codon, and has no internal in-frame stop codons.In general, given a complete CDS, the default translate method will do whatyou want (perhaps with the to_stop option). However, what if yoursequence uses a non-standard start codon? This happens a lot in bacteria for example the gene yaaX in E. coli K12:

.. code-block:: python

    >>> gene = Seq("GTGAAAAAGATGCAATCTATCGTACTCGCACTTTCCCTGGTTCTGGTCGCTCCCATGGCA" + \
    ...            "GCACAGGCTGCGGAAATTACGTTAGTCCCGTCAGTAAAATTACAGATAGGCGATCGTGAT" + \
    ...            "AATCGTGGCTATTACTGGGATGGAGGTCACTGGCGCGACCACGGCTGGTGGAAACAACAT" + \
    ...            "TATGAATGGCGAGGCAATCGCTGGCACCTACACGGACCGCCGCCACCGCCGCGCCACCAT" + \
    ...            "AAGAAAGCTCCTCATGATCATCACGGCGGTCATGGTCCAGGCAAACATCACCGCTAA",
    ...            generic_dna)
    >>> gene.translate(table="Bacterial")
    Seq('VKKMQSIVLALSLVLVAPMAAQAAEITLVPSVKLQIGDRDNRGYYWDGGHWRDH...HR*',
    HasStopCodon(ExtendedIUPACProtein(), '*')
    >>> gene.translate(table="Bacterial", to_stop=True)
    Seq('VKKMQSIVLALSLVLVAPMAAQAAEITLVPSVKLQIGDRDNRGYYWDGGHWRDH...HHR',
    ExtendedIUPACProtein())


.. In the bacterial genetic code GTG is a valid start codon,and while it does normally encode valine, if used as a start codon itshould be translated as methionine. This happens if you tell Biopython yoursequence is a complete CDS:

In the bacterial genetic code GTG is a valid start codon,and while it does normally encode valine, if used as a start codon itshould be translated as methionine. This happens if you tell Biopython yoursequence is a complete CDS:

.. code-block:: python

    >>> gene.translate(table="Bacterial", cds=True)
    Seq('MKKMQSIVLALSLVLVAPMAAQAAEITLVPSVKLQIGDRDNRGYYWDGGHWRDH...HHR',
    ExtendedIUPACProtein())


.. In addition to telling Biopython to translate an alternative start codon asmethionine, using this option also makes sure your sequence really is a validCDS (you’ll get an exception if not).

In addition to telling Biopython to translate an alternative start codon asmethionine, using this option also makes sure your sequence really is a validCDS (you’ll get an exception if not).

.. The example in Section 16.1.2 combines the Seq object’s translate method with Bio.SeqIO for sequence input/ouput.

The example in Section 16.1.2 combines the Seq object’s translate method with Bio.SeqIO for sequence input/ouput.

.. Note: The Seq object’s translate method is new in Biopython 1.49.For older releases you would have to use the Bio.Seq module’s translatefunction instead, see Section 3.14. The cds optionwas added in Biopython 1.51, and there is no simple way to do this with older versionsof Biopython.

Note: The Seq object’s translate method is new in Biopython 1.49.For older releases you would have to use the Bio.Seq module’s translatefunction instead, see Section 3.14. The cds optionwas added in Biopython 1.51, and there is no simple way to do this with older versionsof Biopython.

.. index::
   pair: 3.10  Translation Tables;3.10  Translation Tables

3.10  翻訳テーブル
------------------------

.. In the previous sections we talked about the Seq object translation method (and mentioned the equivalent function in the Bio.Seq module  seeSection 3.14).Internally these use codon table objects derived from the NCBI information atftp://ftp.ncbi.nlm.nih.gov/entrez/misc/data/gc.prt, also shown onhttp://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi in a much more readable layout.

In the previous sections we talked about the Seq object translation method (and mentioned the equivalent function in the Bio.Seq module  seeSection 3.14).Internally these use codon table objects derived from the NCBI information atftp://ftp.ncbi.nlm.nih.gov/entrez/misc/data/gc.prt, also shown onhttp://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi in a much more readable layout.

.. As before, let’s just focus on two choices: the Standard translation table, and the translation table for Vertebrate Mitochondrial DNA.

前と同じように、標準翻訳テーブルと、Vertebrate Mitochondrial DNAに対する翻訳テーブルの、2つの選択肢に焦点を当てましょう。

.. code-block:: python

    >>> from Bio.Data import CodonTable
    >>> standard_table = CodonTable.unambiguous_dna_by_name["Standard"]
    >>> mito_table = CodonTable.unambiguous_dna_by_name["Vertebrate Mitochondrial"]


.. Alternatively, these tables are labeled with ID numbers 1 and 2, respectively:

また、これらのテーブルには、それぞれ ID番号1と2がついています:

.. code-block:: python

    >>> from Bio.Data import CodonTable
    >>> standard_table = CodonTable.unambiguous_dna_by_id[1]
    >>> mito_table = CodonTable.unambiguous_dna_by_id[2]


.. You can compare the actual tables visually by printing them:

これらを出力することで、実際のテーブルを視覚的に比較することができます:

.. code-block:: python

    >>> print standard_table
    Table 1 Standard, SGC0

      |  T      |  C      |  A      |  G      |
    --+---------+---------+---------+---------+--
    T | TTT F   | TCT S   | TAT Y   | TGT C   | T
    T | TTC F   | TCC S   | TAC Y   | TGC C   | C
    T | TTA L   | TCA S   | TAA Stop| TGA Stop| A
    T | TTG L(s)| TCG S   | TAG Stop| TGG W   | G
    --+---------+---------+---------+---------+--
    C | CTT L   | CCT P   | CAT H   | CGT R   | T
    C | CTC L   | CCC P   | CAC H   | CGC R   | C
    C | CTA L   | CCA P   | CAA Q   | CGA R   | A
    C | CTG L(s)| CCG P   | CAG Q   | CGG R   | G
    --+---------+---------+---------+---------+--
    A | ATT I   | ACT T   | AAT N   | AGT S   | T
    A | ATC I   | ACC T   | AAC N   | AGC S   | C
    A | ATA I   | ACA T   | AAA K   | AGA R   | A
    A | ATG M(s)| ACG T   | AAG K   | AGG R   | G
    --+---------+---------+---------+---------+--
    G | GTT V   | GCT A   | GAT D   | GGT G   | T
    G | GTC V   | GCC A   | GAC D   | GGC G   | C
    G | GTA V   | GCA A   | GAA E   | GGA G   | A
    G | GTG V   | GCG A   | GAG E   | GGG G   | G
    --+---------+---------+---------+---------+--


.. and:

と:

.. code-block:: python

    >>> print mito_table
    Table 2 Vertebrate Mitochondrial, SGC1

      |  T      |  C      |  A      |  G      |
    --+---------+---------+---------+---------+--
    T | TTT F   | TCT S   | TAT Y   | TGT C   | T
    T | TTC F   | TCC S   | TAC Y   | TGC C   | C
    T | TTA L   | TCA S   | TAA Stop| TGA W   | A
    T | TTG L   | TCG S   | TAG Stop| TGG W   | G
    --+---------+---------+---------+---------+--
    C | CTT L   | CCT P   | CAT H   | CGT R   | T
    C | CTC L   | CCC P   | CAC H   | CGC R   | C
    C | CTA L   | CCA P   | CAA Q   | CGA R   | A
    C | CTG L   | CCG P   | CAG Q   | CGG R   | G
    --+---------+---------+---------+---------+--
    A | ATT I(s)| ACT T   | AAT N   | AGT S   | T
    A | ATC I(s)| ACC T   | AAC N   | AGC S   | C
    A | ATA M(s)| ACA T   | AAA K   | AGA Stop| A
    A | ATG M(s)| ACG T   | AAG K   | AGG Stop| G
    --+---------+---------+---------+---------+--
    G | GTT V   | GCT A   | GAT D   | GGT G   | T
    G | GTC V   | GCC A   | GAC D   | GGC G   | C
    G | GTA V   | GCA A   | GAA E   | GGA G   | A
    G | GTG V(s)| GCG A   | GAG E   | GGG G   | G
    --+---------+---------+---------+---------+--


.. You may find these following properties useful  for example if you are trying to do your own gene finding:

You may find these following properties useful  for example if you are trying to do your own gene finding:

.. code-block:: python

    >>> mito_table.stop_codons
    ['TAA', 'TAG', 'AGA', 'AGG']
    >>> mito_table.start_codons
    ['ATT', 'ATC', 'ATA', 'ATG', 'GTG']
    >>> mito_table.forward_table["ACG"]
    'T'


.. index::
   pair: 3.11  Comparing Seq objects;3.11  Comparing Seq objects

3.11  Seq オブジェクトを比較する
--------------------------------

.. Sequence comparison is actually a very complicated topic, and there is no easyway to decide if two sequences are equal. The basic problem is the meaning ofthe letters in a sequence are context dependent - the letter “A” could be partof a DNA, RNA or protein sequence. Biopython uses alphabet objects as part ofeach Seq object to try and capture this information - so comparing twoSeq objects means considering both the sequence strings and thealphabets.

Sequence comparison is actually a very complicated topic, and there is no easyway to decide if two sequences are equal. The basic problem is the meaning ofthe letters in a sequence are context dependent - the letter “A” could be partof a DNA, RNA or protein sequence. Biopython uses alphabet objects as part ofeach Seq object to try and capture this information - so comparing twoSeq objects means considering both the sequence strings and thealphabets.

.. For example, you might argue that the two DNA Seq objectsSeq("ACGT", IUPAC.unambiguous_dna) andSeq("ACGT", IUPAC.ambiguous_dna) should be equal, even thoughthey do have different alphabets. Depending on the context this could beimportant.

For example, you might argue that the two DNA Seq objectsSeq("ACGT", IUPAC.unambiguous_dna) andSeq("ACGT", IUPAC.ambiguous_dna) should be equal, even thoughthey do have different alphabets. Depending on the context this could beimportant.

.. This gets worse  suppose you think Seq("ACGT",IUPAC.unambiguous_dna) and Seq("ACGT") (i.e. the default genericalphabet) should be equal. Then, logically, Seq("ACGT", IUPAC.protein)and Seq("ACGT") should also be equal. Now, in logic if A=B andB=C, by transitivity we expect A=C. So for logical consistency we’drequire Seq("ACGT", IUPAC.unambiguous_dna) and Seq("ACGT",IUPAC.protein) to be equal  which most people would agree is just not right.This transitivity problem would also have implications for using Seqobjects as Python dictionary keys.

This gets worse  suppose you think Seq("ACGT",IUPAC.unambiguous_dna) and Seq("ACGT") (i.e. the default genericalphabet) should be equal. Then, logically, Seq("ACGT", IUPAC.protein)and Seq("ACGT") should also be equal. Now, in logic if A=B andB=C, by transitivity we expect A=C. So for logical consistency we’drequire Seq("ACGT", IUPAC.unambiguous_dna) and Seq("ACGT",IUPAC.protein) to be equal  which most people would agree is just not right.This transitivity problem would also have implications for using Seqobjects as Python dictionary keys.

.. So, what does Biopython do? Well, the equality test is the default for Pythonobjects  it tests to see if they are the same object in memory. This is avery strict test:

So, what does Biopython do? Well, the equality test is the default for Pythonobjects  it tests to see if they are the same object in memory. This is avery strict test:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import IUPAC
    >>> seq1 = Seq("ACGT", IUPAC.unambiguous_dna)
    >>> seq2 = Seq("ACGT", IUPAC.unambiguous_dna)
    >>> seq1 == seq2
    False
    >>> seq1 == seq1
    True


.. If you actually want to do this, you can be more explicit by using the Python id function,

もしこれを本当にやりたいのであれば、Pythonのid関数を使うことで明示的に行うことができます。

.. code-block:: python

    >>> id(seq1) == id(seq2)
    False
    >>> id(seq1) == id(seq1)
    True


.. Now, in every day use, your sequences will probably all have the samealphabet, or at least all be the same type of sequence (all DNA, all RNA, orall protein). What you probably want is to just compare the sequences asstrings  so do this explicitly:

Now, in every day use, your sequences will probably all have the samealphabet, or at least all be the same type of sequence (all DNA, all RNA, orall protein). What you probably want is to just compare the sequences asstrings  so do this explicitly:

.. code-block:: python

    >>> str(seq1) == str(seq2)
    True
    >>> str(seq1) == str(seq1)
    True


.. As an extension to this, while you can use a Python dictionary with Seq objects as keys, it is generally more useful to use the sequence a string for the key. See also Section 3.4.

これを拡張して、SeqオブジェクトをPythonの辞書のキーにすることができます。一般的にキーとして文字列を用いるより便利です。Section 3.4 を見てください。

.. index::
   pair: 3.12  MutableSeq objects;3.12  MutableSeq objects

3.12  MutableSeq objects
------------------------

.. Just like the normal Python string, the Seq object is “read only”, or in Python terminology, immutable. Apart from wanting the Seq object to act like a string, this is also a useful default since in many biological applications you want to ensure you are not changing your sequence data:

通常のPython文字列のように、Seqオブジェクトは"読み込み専用"です。Pythonでいうところのimmutableです。 SeqオブジェクトがPythonのstringのように振る舞うことから離れたとしても、たくさんの生物学的アプリケーションで、シーケンスデータが変更されないことを確認することができるので便利です:

.. code-block:: python

    >>> from Bio.Seq import Seq
    >>> from Bio.Alphabet import IUPAC
    >>> my_seq = Seq("GCCATTGTAATGGGCCGCTGAAAGGGTGCCCGA", IUPAC.unambiguous_dna)
    >>> my_seq[5] = "G"
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    AttributeError: 'Seq' instance has no attribute '__setitem__'


.. However, you can convert it into a mutable sequence (a MutableSeq object) and do pretty much anything you want with it:

しかしながら、これを変更可能なシーケンス(MutableSeqオブジェクト)へ変更することも可能で、なんでも行うことができます:

.. code-block:: python

    >>> mutable_seq = my_seq.tomutable()
    >>> mutable_seq
    MutableSeq('GCCATTGTAATGGGCCGCTGAAAGGGTGCCCGA', IUPACUnambiguousDNA())


.. Alternatively, you can create a MutableSeq object directly from a string:

また、文字列から直接 MutableSeq オブジェクトを作ることができます:

.. code-block:: python

    >>> from Bio.Seq import MutableSeq
    >>> from Bio.Alphabet import IUPAC
    >>> mutable_seq = MutableSeq("GCCATTGTAATGGGCCGCTGAAAGGGTGCCCGA", IUPAC.unambiguous_dna)


.. Either way will give you a sequence object which can be changed:

いずれかの方法で、変更可能なシーケンスオブジェクトを取得できます:

.. code-block:: python

    >>> mutable_seq
    MutableSeq('GCCATTGTAATGGGCCGCTGAAAGGGTGCCCGA', IUPACUnambiguousDNA())
    >>> mutable_seq[5] = "T"
    >>> mutable_seq
    MutableSeq('GCCATTGTAATGGGCCGCTGAAAGGGTGCCCGA', IUPACUnambiguousDNA())
    >>> mutable_seq.remove("T")
    >>> mutable_seq
    MutableSeq('GCCATGTAATGGGCCGCTGAAAGGGTGCCCGA', IUPACUnambiguousDNA())
    >>> mutable_seq.reverse()
    >>> mutable_seq
    MutableSeq('AGCCCGTGGGAAAGTCGCCGGGTAATGTACCG', IUPACUnambiguousDNA())


.. Do note that unlike the Seq object, the MutableSeq object’s methods like reverse_complement() and reverse() act in-situ!

Seqオブジェクトと違って、MutableSeqのreverse_complement()やreverse()のようなメソッドは、その場で実行されます!

.. An important technical difference between mutable and immutable objects in Python means that you can’t use a MutableSeq object as a dictionary key, but you can use a Python string or a Seq object in this way.

Pythonでの mutable と immutable のオブジェクトの技術的で重要な違いは、MutableSeqは、辞書のキーにすることができません、しかし、この方法でPythonの文字列またはSeqオブジェクトを使うことができます。

.. Once you have finished editing your a MutableSeq object, it’s easy to get back to a read-only Seq object should you need to:

MutableSeqオブジェクトを編集し終えたら、読み込み専用のSeqオブジェクトを簡単に取り出すことができます:

.. code-block:: python

    >>> new_seq = mutable_seq.toseq()
    >>> new_seq
    Seq('AGCCCGTGGGAAAGTCGCCGGGTAATGTACCG', IUPACUnambiguousDNA())


.. You can also get a string from a MutableSeq object just like from a Seq object (Section 3.4).

またMutableSeqオブジェクトも、Seqオブジェクトのように(Section 3.4)文字列を取得することができます。

.. index::
   pair: 3.13  UnknownSeq objects;3.13  UnknownSeq objects

3.13  UnknownSeq オブジェクト
-----------------------------

.. Biopython 1.50 introduced another basic sequence object, the UnknownSeq object.This is a subclass of the basic Seq object and its purpose is to represent asequence where we know the length, but not the actual letters making it up.You could of course use a normal Seq object in this situation, but it wastesrather a lot of memory to hold a string of a million “N” characters when you couldjust store a single letter “N” and the desired length as an integer.

Biopython 1.50 introduced another basic sequence object, the UnknownSeq object.This is a subclass of the basic Seq object and its purpose is to represent asequence where we know the length, but not the actual letters making it up.You could of course use a normal Seq object in this situation, but it wastesrather a lot of memory to hold a string of a million “N” characters when you couldjust store a single letter “N” and the desired length as an integer.

.. code-block:: python

    >>> from Bio.Seq import UnknownSeq
    >>> unk = UnknownSeq(20)
    >>> unk
    UnknownSeq(20, alphabet = Alphabet(), character = '?')
    >>> print unk
    ????????????????????
    >>> len(unk)
    20


.. You can of course specify an alphabet, meaning for nucleotide sequencesthe letter defaults to “N” and for proteins “X”, rather than just “?”.

You can of course specify an alphabet, meaning for nucleotide sequencesthe letter defaults to “N” and for proteins “X”, rather than just “?”.

.. code-block:: python

    >>> from Bio.Seq import UnknownSeq
    >>> from Bio.Alphabet import IUPAC
    >>> unk_dna = UnknownSeq(20, alphabet=IUPAC.ambiguous_dna)
    >>> unk_dna
    UnknownSeq(20, alphabet = IUPACAmbiguousDNA(), character = 'N')
    >>> print unk_dna
    NNNNNNNNNNNNNNNNNNNN


.. You can use all the usual Seq object methods too, note these give back memory saving UnknownSeq objects where appropriate as you might expect:

You can use all the usual Seq object methods too, note these give back memory saving UnknownSeq objects where appropriate as you might expect:

.. code-block:: python

    >>> unk_dna
    UnknownSeq(20, alphabet = IUPACAmbiguousDNA(), character = 'N')
    >>> unk_dna.complement()
    UnknownSeq(20, alphabet = IUPACAmbiguousDNA(), character = 'N')
    >>> unk_dna.reverse_complement()
    UnknownSeq(20, alphabet = IUPACAmbiguousDNA(), character = 'N')
    >>> unk_dna.transcribe()
    UnknownSeq(20, alphabet = IUPACAmbiguousRNA(), character = 'N')
    >>> unk_protein = unk_dna.translate()
    >>> unk_protein
    UnknownSeq(6, alphabet = ProteinAlphabet(), character = 'X')
    >>> print unk_protein
    XXXXXX
    >>> len(unk_protein)
    6


.. You may be able to find a use for the UnknownSeq object in your owncode, but it is more likely that you will first come across them in aSeqRecord object created by Bio.SeqIO(see Chapter 5).Some sequence file formats don’t always include the actual sequence, forexample GenBank and EMBL files may include a list of features but for thesequence just present the contig information. Alternatively, the QUAL filesused in sequencing work hold quality scores but they never contain asequence  instead there is a partner FASTA file which does have thesequence.

You may be able to find a use for the UnknownSeq object in your owncode, but it is more likely that you will first come across them in aSeqRecord object created by Bio.SeqIO(see Chapter 5).Some sequence file formats don’t always include the actual sequence, forexample GenBank and EMBL files may include a list of features but for thesequence just present the contig information. Alternatively, the QUAL filesused in sequencing work hold quality scores but they never contain asequence  instead there is a partner FASTA file which does have thesequence.

.. index::
   pair: 3.14  Working with directly strings;3.14  Working with directly strings

3.14  Working with directly strings
-----------------------------------

.. To close this chapter, for those you who really don’t want to use the sequenceobjects (or who prefer a functional programming style to an object orientated one),there are module level functions in Bio.Seq will accept plain Python strings,Seq objects (including UnknownSeq objects) or MutableSeq objects:

To close this chapter, for those you who really don’t want to use the sequenceobjects (or who prefer a functional programming style to an object orientated one),there are module level functions in Bio.Seq will accept plain Python strings,Seq objects (including UnknownSeq objects) or MutableSeq objects:

.. code-block:: python

    >>> from Bio.Seq import reverse_complement, transcribe, back_transcribe, translate
    >>> my_string = "GCTGTTATGGGTCGTTGGAAGGGTGGTCGTGCTGCTGGTTAG"
    >>> reverse_complement(my_string)
    'CTAACCAGCAGCACGACCACCCTTCCAACGACCCATAACAGC'
    >>> transcribe(my_string)
    'GCUGUUAUGGGUCGUUGGAAGGGUGGUCGUGCUGCUGGUUAG'
    >>> back_transcribe(my_string)
    'GCTGTTATGGGTCGTTGGAAGGGTGGTCGTGCTGCTGGTTAG'
    >>> translate(my_string)
    'AVMGRWKGGRAAG*'


.. You are, however, encouraged to work with Seq objects by default.

You are, however, encouraged to work with Seq objects by default.

